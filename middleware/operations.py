import random

from main import MWare

# redis/utils.py
try:
    import hiredis  # hiredis as minimalistic C client library for the Redis database

    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False


def get_from(*key_list):
    res = {}
    for key in key_list:
        res[key] = MWare.redis_db.get(key)

    return res


def set_values(*value_list):
    #   redis_db.mset({key: value for key, value in key_value_list.items()})
    with MWare.redis_db.pipeline() as pipe:
        for value in value_list:
            pipe.set(str(random.getrandbits(8)), value)
        pipe.execute()


def update(*key):
    pass


def delete_keys(*key_list):
    with MWare.redis_db.pipeline() as pipe:
        for key in key_list:
            pipe.delete(key)
        pipe.execute()


def flush_db():
    MWare.redis_db.flushdb()
    # MWare.
