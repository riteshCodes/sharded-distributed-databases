import random

import redis

# redis/utils.py
try:
    import hiredis  # hiredis as minimalistic C client library for the Redis database

    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False


class MWare:

    def __init__(self, *, client_id: int, port_nr: int = 6379, site_count: int = 1, db_id: int = 0):
        """
        init
        :param client_id:
        :param site_count: site_count = 1; default number of sites (single site)
        :param db_id:
        """
        # redis_instances = 1; default number of redis instance
        # redis database, config file: /etc/redis/6379.conf
        self.pool = redis.ConnectionPool(host='localhost', port=port_nr, db=db_id, decode_responses=True)
        self.redis_db = redis.StrictRedis(
            connection_pool=self.pool)
        self.client_id = client_id
        self.db_id = db_id
        self.site_count = site_count

    def connect_db(self):
        pass

    def set_site(self, site_count):
        self.site_count = site_count

    def get_all(self, *, hash_key_list: list = None):
        """
        get_all
        :param hash_key_list:
        :return:
        """
        if hash_key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')
        res = []
        for hash_key in hash_key_list:
            key = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            hash_values = self.redis_db.hgetall(key)
            res.append(hash_values)
        return res

    def get_fields(self, *, hash_key: int = None, field_list: list = None):
        """
        get_fields
        :param hash_key:
        :param field_list:
        :return:
        """
        if hash_key is None or field_list is None:
            raise TypeError('None type passed as argument')
        val = []
        for field in field_list:
            key = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            hash_values = self.redis_db.hget(key, field)
            val.append(hash_values)
        return val

    def set_to(self, *, hash_key=random.getrandbits(8), **mapping):
        """
        set_to
        :param hash_key:
        :param mapping:
        :return:
        """
        if mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')
        key = 'Client:' + str(self.client_id) + ':' + str(hash_key)
        self.redis_db.hset(key, mapping=mapping)
        return hash_key

    def set_multiple(self, hash_key_list: list = None, **mapping):
        """
        set_multiple
        :param hash_key_list:
        :param mapping:
        :return:
        """
        if hash_key_list is None or mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')
        key_list = []
        for hash_key in hash_key_list:
            k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            key_list.append(k)

        with self.redis_db.pipeline() as pipe:
            for key in key_list:
                pipe.hset(key, mapping=mapping)
            pipe.execute()

    def del_fields(self, *, hash_key: int = None, fields: list = None):
        """
        del_fields
        :param hash_key:
        :param fields:
        :return:
        """
        if hash_key is None or fields is None:
            raise TypeError('None type passed as argument.')

        key = 'Client:' + str(self.client_id) + ':' + str(hash_key)
        with self.redis_db.pipeline() as pipe:
            for field in fields:
                pipe.hdel(key, field)
            pipe.execute()

    def del_keys(self, *, hash_key_list: list = None):
        """
        del_keys
        :param hash_key_list:
        :return:
        """
        if hash_key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        key_list = []
        for hash_key in hash_key_list:
            key = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            key_list.append(key)

        self.redis_db.delete(*key_list)

    def flush_db(self):
        """
        flush_db
        :return:
        """
        self.redis_db.flushdb()


if __name__ == '__main__':
    print("MWare is running")
