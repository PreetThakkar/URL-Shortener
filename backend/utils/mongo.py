# standard imports
from datetime import datetime, timezone
from typing import Dict
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

def insert_url_info(mon_con: MongoClient, short_url: str, info: Dict):
    mon_db: Database = mon_con["url_db"]
    mon_db["urls"].update_one(
        filter={
            "_id": short_url,
        },
        update={
            "$set": info
        },
        upsert=True
    )