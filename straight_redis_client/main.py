import redis
from configs import REDIS_DB_URL


class RedisClient:
    """
    RedisClient: A redis client using redis-py python interface to operate with single Redis key-value store
    """

    def __init__(self):
        """
        init initializes configurations (physical nodes' url, number of virtual nodes, responses) for redis connection
        pool, using StrictRedis protocol from redis-py python interface.
        """

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
        result = []
        keys = uid(k_list=key_list)
        if len(key_list) == 1:
            result.append(self.redis_db.hgetall(keys))
        else:
            with self.redis_db.pipeline() as pipe:
                for k in keys:
                    pipe.hgetall(k)
                result += pipe.execute()
        return result

    def get_fields(self, *, key_list: list = None, field_list: list = None):
        """
        get_fields (projection) returns all the fields values from the given key in the database
        :param key_list: key from which data is fetched
        :param field_list: fields of the keys from where data is fetched
        :return:
        """
        result = []
        keys = uid(k_list=key_list)

        for k in keys:
            result.append(self.redis_db.hmget(k, field_list))

        return result

    def get_range(self, *, start: int = 0, end: int):
        """
        get_range (selection) retrieves all key-value pairs from keys from range (inclusive) [start, end]
        :param start: start index key
        :param end: end index key
        :return:
        """
        result = []

        keys = uid(k_list=[*range(start, end + 1)])
        if end == 0:
            result.append(self.redis_db.hgetall(keys))

        else:
            with self.redis_db.pipeline() as pipe:
                for k in keys:
                    pipe.hgetall(k)
                result += pipe.execute()

        return result

    def set_to(self, *, key: int, **mapping):
        """
        set_to (insertion) sets/updates the value to the given key in the database
        :param key: key where the mapping is stored
        :param mapping: dict (key-value pairs) for storing the data
        :return:
        """
        k = uid(k_list=[key])
        self.redis_db.hset(k, mapping=mapping)

        return 'OK'

    def set_multiples(self, key_list: list = None, name_list: list = None, email_list: list = None):
        """
        set_to (bulk insertion) sets/updates the value to the given key in the database
        :param key_list: key where the mapping is stored
        :param name_list:
        :param email_list:
        :return:
        """
        keys = uid(k_list=key_list)
        with self.redis_db.pipeline() as pipe:
            for k, n, e in zip(keys, name_list, email_list):
                pipe.hset(k, mapping={'name': n, 'email': e})
            pipe.execute()
        return 'OK'

    def update_values(self, key_list: list = None, **mapping):
        """
        update_values (bulk update) updates/creates fields and values (as mapping/dict) to multiple given keys in the
        database. If the keys are not present in the database, new keys are created
        :param key_list: list of keys, where the mapping is added/updated
        :param mapping: dict as key-value pair
        :return: None
        """
        keys = uid(k_list=key_list)
        for k in keys:
            self.redis_db.hset(k, mapping=mapping)
        return 'OK'

    def del_fields(self, *, key_list: list = None, fields: list = None):
        """
        del_fields (field deletion) deletes the fields from the passed key_list from the database
        :param key_list: keys to delete as list
        :param fields: fields from the key to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        keys = uid(k_list=key_list)

        for k in keys:
            self.redis_db.hdel(k, *fields)

        return 'OK'

    def del_keys(self, *, key_list: list = None):
        """
        del_keys (deletion) deletes all given key list from the database
        :param key_list: key list to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        keys = uid(k_list=key_list)
        if len(key_list) == 1:
            self.redis_db.delete(keys)
        else:
            with self.redis_db.pipeline() as pipe:
                for k in keys:
                    pipe.delete(k)
                pipe.execute()

        return 'OK'

    def flush_all(self):
        """
        flush_all wipes all data from all database instances
        :return: None
        """
        self.redis_db.flushall()
        return 'OK'

    def key_space_inf(self):
        """
        key_space_inf returns the total number of keys present in each site
        :return: key-value pairs (dict) with key as site and value as total number of keys present
        """
        inf = {REDIS_DB_URL: self.redis_db.dbsize()}

        return inf


def uid(*, k_list: list):
    if len(k_list) == 0:
        return KeyError('Key list is empty')
    elif len(k_list) == 1:
        return 'userID' + ':' + '{:04d}'.format(k_list[0])

    else:
        return ['userID' + ':' + '{:04d}'.format(k) for k in k_list]
