# third party imports
from redis import StrictRedis
# local imports
from settings import REDIS_HOST, REDIS_PORT, REDIS_PASS

def get_redis_con():
    return StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)