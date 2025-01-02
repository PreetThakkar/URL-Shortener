# standard imports
from datetime import datetime, timezone
# third party imports
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
# local imports
from settings import MONGO_URI

def get_mon_con():
    return MongoClient(MONGO_URI)

def get_url_info(mon_con: MongoClient, short_url: str):
    query = {
        "_id": short_url
    }
    mon_db: Database = mon_con["url_db"]

    results = list(mon_db["urls"].find(query))
    if not results:
        return None

    return results[0]

def insert_url_info(mon_con: MongoClient, short_url: str, url: str):
    update = {
        "$set": {
            "url": url,
            "last_accessed": datetime.now(tz=timezone.utc),
            "visits": 0
        },
        "$setOnInsert": {
            "created_at": datetime.now(tz=timezone.utc)
        }
    }
    
    # Only updating the visit count
    if not url:
        update["$set"].pop("visits")
        update["$inc"] = {"visits": 1}
        update["$set"].pop("url")

    
    mon_db: Database = mon_con["url_db"]
    mon_db["urls"].update_one(
        filter={
            "_id": short_url,
        },
        update=update,
        upsert=True
    )