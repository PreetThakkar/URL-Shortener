# standard imports
from datetime import datetime
from time import sleep
# third party imports
from pymongo.mongo_client import MongoClient
from redis import StrictRedis
# local imports
from utils.mongo import get_mon_con, insert_url_info
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASS

def get_redis_con():
    return StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)

def update_mongo(redis_con: StrictRedis, mon_con: MongoClient):
    date_transform = lambda x: datetime.fromisoformat(x)
    int_transform = lambda x: int(x)
    tts = 30 # time to sleep
    
    def iteration():
        for short_url in redis_con.hkeys("mongo"):
            print(f"[{short_url}] Processing short_url")
            url_info = redis_con.hgetall(short_url)

            # Data type management
            field_func_map = {
                "last_accessed": date_transform,
                "created_at": date_transform,
                "visits": int_transform
            }
            for field, transform in field_func_map.items():
                if field not in url_info or not url_info.get(field): 
                    continue
                print(f"[{short_url}] Transforming field: {field}")
                url_info[field] = transform(url_info[field])

            # Write to mongo
            print(f"[{short_url}] Writing data to Mongo")
            insert_url_info(mon_con, short_url, url_info)
            
            # Pop from queue
            print(f"[{short_url}] Mongo and Redis in sync for this short_url")
            redis_con.hdel("mongo", short_url)
            
    while True:
        iteration()
        print(f"Sleeping for {tts} seconds")
        sleep(tts)

if __name__ == "__main__":
    redis_con = get_redis_con()
    mon_con = get_mon_con()
    update_mongo(redis_con, mon_con)
