# standard imports
from json import dumps
from http import HTTPStatus
# third party imports
from flask import Flask, Response, redirect, request
from flask.views import MethodView
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
# local imports
from utils.mongo import get_mon_con, get_url_info, insert_url_info
from utils.shortner import shorten

app = Flask(__name__)
CORS(app)
mon_con = get_mon_con()

class ShortUrl(MethodView):
    def get(self, short_url):
        app.logger.info(f"Requested original url for: {short_url}")
        
        # Check if short url exists
        url_info = get_url_info(mon_con, short_url)
        if not url_info:
            # Return 404 not found
            return Response(
                response="URL not found",
                status=HTTPStatus.NOT_FOUND
            )

        # Update visit counts
        insert_url_info(mon_con, short_url, None)

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
            
            # Insert record in database
            insert_url_info(mon_con, short_url, url)

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
        
        # Check if short url exists
        url_info = get_url_info(mon_con, short_url)
        if not url_info:
            # Return 404 not found
            return Response(
                response="URL not found",
                status=HTTPStatus.NOT_FOUND
            )

        # Return redirect code with original url
        _ = [url_info.update({key: url_info[key].isoformat()}) for key in ("created_at", "last_accessed")]
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