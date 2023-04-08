import json

import redis

from configs import REDIS_DB_URL


class RedisClient:
    """
    RedisClient: A redis client using redis-py python interface to operate with single Redis key-value store
    """

    def __init__(self, hash_key):
        """
        init initializes configurations (physical nodes' url, number of virtual nodes, responses) for redis connection
        pool, using StrictRedis protocol from redis-py python interface.
        """
        self.hash_key = hash_key
        self.redis_db = redis.StrictRedis(
            connection_pool=redis.ConnectionPool.from_url(REDIS_DB_URL, decode_responses=True))

    def ping(self):
        return self.redis_db.ping()

    def get_all(self, *, key_list: list = None):
        """
        get_all (selection) retrieves all key-value pairs (data) from the given key_list in the database
        :param key_list: list of keys from which data is fetched
        :return: mapping of the values as dict or KeyError: if the key is not present in the database
        """
        return self.redis_db.hmget(self.hash_key, key_list)

    def get_range(self, *, start: int = 0, end: int):
        """
        get_range (selection) retrieves all key-value pairs from keys from range (inclusive) [start, end]
        :param start: start index key
        :param end: end index key
        :return: list of key-value pairs
        """
        result = []

        keys = [*range(start, end + 1)]
        result.append(self.redis_db.hmget(self.hash_key, keys))
        return result

    def set_to(self, key, mapping: dict):
        """
        set_to (insertion) sets/updates the value to the given key in the database
        :param key: key where the mapping is stored
        :param mapping: dict (key-value pairs) for storing the data
        :return:
        """
        self.redis_db.hset(self.hash_key, str(key), json.dumps(mapping))

        return 'OK'

    def set_multiples(self, *, content: dict):
        """
        set_to (bulk insertion) sets/updates the value to the given key in the database
        :param content: worload
        :return:
        """
        with self.redis_db.pipeline(transaction=True) as pipe:
            for key, value in content.items():
                pipe.hset(self.hash_key, key, json.dumps(content))
            pipe.execute()
        return 'OK'

    def del_keys(self, *, key_list: list = None):
        """
        del_keys (deletion) deletes all given key list from the database
        :param key_list: key list to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        self.redis_db.hdel(self.hash_key, *key_list)
        return 'OK'
