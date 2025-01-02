# standard imports
from datetime import datetime, timezone
from json import dumps
from http import HTTPStatus
# third party imports
from flask import Flask, Response, redirect, request
from flask.views import MethodView
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
# local imports
from utils.mongo import get_mon_con, get_url_info
from utils.redis import get_redis_con
from utils.shortner import shorten

app = Flask(__name__)
CORS(app)
mon_con = get_mon_con()
redis_con = get_redis_con()

class ShortUrl(MethodView):
    def get(self, short_url):
        app.logger.info(f"Requested original url for: {short_url}")
        
        # Check if short url exists: Redis
        app.logger.debug(f"Fetching data from Redis: {short_url}")
        url_info = redis_con.hgetall(short_url)
        if not url_info:
            # Fetch url info: Mongo
            app.logger.debug(f"Fetching data from Mongo: {short_url}")
            url_info = get_url_info(mon_con, short_url)

            # Update datetime objects to isoformat strings
            _ = [url_info.update({x: url_info[x].isoformat()}) for x in ("last_accessed", "created_at") if url_info[x].__class__ == datetime]
            if not url_info:
                # Return 404 not found
                return Response(
                    response="URL not found",
                    status=HTTPStatus.NOT_FOUND
                )
            
            # Update info: Redis
            redis_con.hmset(short_url, url_info)
        
        # Update visit counts
        url_update = {
            "visits": int(url_info["visits"]) + 1,
            "last_accessed": datetime.now(tz=timezone.utc).isoformat()
        }
        redis_con.hmset("mongo", { short_url: 1 })
        redis_con.hmset(short_url, url_update)

        # Return redirect code with original url
        return redirect(url_info["url"], code=HTTPStatus.FOUND)
    
    def post(self, **args):
        # Default values for response variables
        short_url, message, status = None, None, HTTPStatus.INTERNAL_SERVER_ERROR

        url = request.json.get("url")
        app.logger.info(f"Shortening URL: {url}")
        try:
            # Shorten the url
            short_url = shorten(url)

            # Insert record: Redis
            redis_con.hmset("mongo", {short_url: 1})
            redis_con.hmset(short_url, {
                "url": url,
                "visits": 0,
                "created_at": datetime.now(tz=timezone.utc).isoformat()
            })

            status = HTTPStatus.OK
        except Exception as e:
            app.logger.error("Error generating short url", exc_info=True)
            message = "Failed to shorten the provided URL"
        
        # Return the short url
        return Response(
            response=dumps({
                "short_url": short_url,
                "message": message
            }),
            status=status,
            content_type="application/json"
        )

class URLStats(MethodView):
    def post(self):
        short_url = request.json.get("url")
        app.logger.info(f"Requested original url for: {short_url}")
        
        # Check if short url exists: Redis
        app.logger.debug(f"Fetching data from Redis: {short_url}")
        url_info = redis_con.hgetall(short_url)
        if not url_info:
            # Check url info: Mongo
            app.logger.debug(f"Fetching data from Mongo: {short_url}")
            url_info = get_url_info(mon_con, short_url)

            # Update datetime objects to isoformat strings
            _ = [url_info.update({x: url_info[x].isoformat()}) for x in ("last_accessed", "created_at") if url_info[x].__class__ == datetime]
            if not url_info:
                # Return 404 not found
                return Response(
                    response="URL not found",
                    status=HTTPStatus.NOT_FOUND
                )

        # Return redirect code with original url
        return Response(
            response=dumps({
                "info": url_info
            }),
            status=HTTPStatus.OK,
            content_type="application/json",
        )

app.add_url_rule("/", view_func=ShortUrl.as_view("url-post")) 
app.add_url_rule("/<string:short_url>", view_func=ShortUrl.as_view("url"))
app.add_url_rule("/stats", view_func=URLStats.as_view("stats"))