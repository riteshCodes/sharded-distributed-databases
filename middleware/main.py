import time

import redis

from configs import DB_NODES, VIRTUAL_NODES
from sharding import ConsistentHashSharder
from logger import log_execution_time

import inspect  # for decorator


class MWare:
    """
    Mware Class: Middleware, a layer between (python) clients and (Redis key-value store) distributed databases,
                 responsible for fetching, storing and manipulating data.
    """

    def __init__(self):
        """
        init initializes configurations (physical nodes' url, number of virtual nodes, responses) for redis connection
        pool, using StrictRedis protocol from redis-py python interface.
        """
        self.redis_db = {}
        self.sharder = ConsistentHashSharder(virtual_nodes=VIRTUAL_NODES)
        for site in DB_NODES:
            self.sharder.add_node(node_url=site)
            self.redis_db[site] = redis.StrictRedis(
                connection_pool=redis.ConnectionPool.from_url(site, decode_responses=True))

    def start_pipeline(self):
        """
        start_pipeline
        """
        pipe = {}
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)
        return pipe

    def get_single(self, *, key_list: list = None):
        keys = uid(k_list=key_list)

        node = self.sharder.get_node_url(shard_key=keys[0])

        return [self.redis_db[node].hgetall(keys[0])]

    def get_multiple(self, *, key_list: list = None):
        """
        get_all (selection) retrieves all key-value pairs (data) from the given key_list in the database
        :param key_list: list of keys from which data is fetched
        :return: mapping of the values as dict or KeyError: if the key is not present in the database
        """
        result = []
        pipe = {}
        keys = uid(k_list=key_list)

        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hgetall(k)

        for p in pipe.values():
            result += p.execute()
            p.close()

        return result

    def get_fields(self, *, key_list: list = None, field_list: list = None):
        """
        get_fields (projection) returns all the fields values from the given key in the database
        :param key_list: key from which data is fetched
        :param field_list: fields of the keys from where data is fetched
        :return:
        """
        if key_list is None or field_list is None:
            raise TypeError('None type passed as argument')

        db_keys = uid(k_list=key_list)
        pipe = self.start_pipeline()
        res = []

        for k in db_keys:
            try:
                node = self.sharder.get_node_url(shard_key=k)
                pipe[node].hmget(k, field_list)
            except KeyError as err:
                print(k, 'does not exist. Exception:', err)

        for p in pipe.values():
            res += p.execute()
            p.close()

        return res

    def get_range(self, *, start: int = 0, end: int):
        """
        get_range (selection) retrieves all key-value pairs from keys from range (inclusive) [start, end]
        :param start: start index key
        :param end: end index key
        :return:
        """
        res = []
        pipe = {}

        keys = uid(k_list=[*range(start, end + 1)])
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hgetall(k)

        for p in pipe.values():
            res += p.execute()
            p.close()
        return res

    def set_to(self, *, key: int, **mapping):
        """
        set_to (insertion) sets/updates the value to the given key in the database
        :param key: key where the mapping is stored
        :param mapping: dict (key-value pairs) for storing the data
        :return:
        """
        if mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')

        k = 'userID' + ':' + '{:04d}'.format(key)
        site_id = self.sharder.get_node_url(shard_key=k)
        self.redis_db[site_id].hset(k, mapping=mapping)

        return 'OK'

    def set_multiples(self, key_list: list = None, name_list: list = None, email_list: list = None):
        """
        set_to (bulk insertion) sets/updates the value to the given key in the database
        :param key_list: key where the mapping is stored
        :param name_list:
        :param email_list:
        :return:
        """
        pipe = {}
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        keys = uid(k_list=key_list)
        for k, n, e in zip(keys, name_list, email_list):
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hset(k, mapping={'name': n, 'email': e})

        for p in pipe.values():
            p.execute(), p.close()

        return 'OK'

    def update_values(self, key_list: list = None, **mapping):
        """
        update_values (bulk update) updates/creates fields and values (as mapping/dict) to multiple given keys in the
        database. If the keys are not present in the database, new keys are created
        :param key_list: list of keys, where the mapping is added/updated
        :param mapping: dict as key-value pair
        :return: None
        """
        if key_list is None or mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')

        pipe = self.start_pipeline()
        keys = uid(k_list=key_list)
        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hset(k, mapping=mapping)

        for p in pipe.values():
            p.execute(), p.close()

        return 'OK'

    def del_fields(self, *, key_list: list = None, fields: list = None):
        """
        del_fields (field deletion) deletes the fields from the passed key_list from the database
        :param key_list: keys to delete as list
        :param fields: fields from the key to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if key_list is None or fields is None:
            raise TypeError('None type passed as argument.')

        db_keys = uid(k_list=key_list)
        pipe = self.start_pipeline()

        for k in db_keys:
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hdel(k, *fields)

        for p in pipe.values():
            p.execute(), p.close()

        return 'OK'

    def del_multiple(self, *, key_list: list = None):
        """
        del_keys (deletion) deletes all given key list from the database
        :param key_list: key list to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        pipe = {}
        keys = uid(k_list=key_list)
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].delete(k)

        for p in pipe.values():
            p.execute(), p.close()

        return 'OK'

    def del_single(self, *, key_list: list = None):
        """
        del_single (deletion) delete given single key from key list from the database
        :param key_list: key list to delete (with single key)
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')
        keys = uid(k_list=key_list)

        node = self.sharder.get_node_url(shard_key=keys[0])
        self.redis_db[node].delete(keys[0])

        return 'OK'

    def flush_all(self):
        """
        flush_all wipes all data from all database instances
        :return: None
        """
        for db_nodes in self.redis_db.values():
            assert db_nodes.flushdb()

        return 'OK'

    def key_space_inf(self):
        """
        key_space_inf returns the total number of keys present in each site
        :return: key-value pairs (dict) with key as site and value as total number of keys present
        """
        inf = {}
        for site_id in self.redis_db.keys():
            inf[site_id] = self.redis_db[site_id].dbsize()

        return inf


def uid(*, k_list: list):
    if len(k_list) == 0:
        return KeyError('Key list is empty')
    else:
        return ['userID' + ':' + '{:04d}'.format(k) for k in k_list]


for name, fct in inspect.getmembers(MWare, inspect.isfunction):
    if name == '__init__' or name == 'start_pipeline':
        pass
    else:
        setattr(MWare, name, log_execution_time(fct))
