import random
import redis

from configs import DB_NODES, VIRTUAL_NODES
from sharding import ConsistentHashSharder


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

    def get_all(self, *, key_list: list = None):
        """
        get_all retrieves all key-value pairs (data) from the given key_list in the database
        :param key_list: list of keys from which data is fetched
        :return: mapping of the values as dict or KeyError: if the key is not present in the database
        """
        """
        if hash_key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        res = []
        for hash_key in hash_key_list:
            k = 'userID' + ':' + str(hash_key)

            try:
                # TODO check if key exists in the database
                site_id = self.sharder.get_node_url(shard_key=k)
                hash_values = self.redis_db[site_id].hgetall(k)
                res.append(hash_values)
            except KeyError as err:
                print(k, 'does not exist. Exception:', err)

        return res
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

    def get_fields(self, *, hash_key: int = None, field_list: list = None):
        """
        get_fields returns all the fields values from the given key in the database
        :param hash_key: key from which data is fetched
        :param field_list: fields of the keys from where data is fetched
        :return:
        """
        if hash_key is None or field_list is None:
            raise TypeError('None type passed as argument')

        k = 'userID' + ':' + str(hash_key)

        try:
            site_id = self.sharder.get_node_url(shard_key=k)
            return self.redis_db[site_id].hmget(k, field_list)
        except KeyError as err:
            print(k, 'does not exist. Exception:', err)

    def set_to(self, *, hash_key=random.getrandbits(8), **mapping):
        """
        set_to sets/updates the value to the given key in the database
        :param hash_key: key where the mapping is stored
        :param mapping: dict (key-value pairs) for storing the data
        :return: hash-key stored in the database
        """
        if mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')

        k = 'userID' + ':' + str(hash_key)

        site_id = self.sharder.get_node_url(shard_key=k)
        # self.table.set_site(key=k)
        # site_id = self.table.get_site(key=k)

        self.redis_db[site_id].hset(k, mapping=mapping)

        return hash_key

    def st_multiple(self, hash_key_list: list = None, **mapping):
        """
        set_multiple sets values (as mapping/dict) to multiple given keys in the database. If the keys are not
        present in the database, new keys are created
        :param hash_key_list: list of keys, where the mapping is added/updated
        :param mapping: dict as key-value pair
        :return: None
        """
        print(mapping)
        if hash_key_list is None or mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')
        # site_key_list = []
        for hash_key in hash_key_list:
            k = 'userID' + ':' + str(hash_key)
            site_id = self.sharder.get_node_url(shard_key=k)
            # self.table.set_site(key=k)
            # site_id = self.table.get_site(key=k)
            # site_key_list.append((site_id, k)) # OLD
            self.redis_db[site_id].hset(k, mapping=mapping)
        """
        for hash_key in hash_key_list:
            k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            self.table.set_site(key=k)
            site_id = self.table.get_site(key=k)
            # site_key_list.append((site_id, k))
            self.redis_db[site_id].hset(k, mapping=mapping)

        # with self.redis_db.pipeline() as pipe:
        #     for v in site_key_list:
        #         pipe.hset(key, mapping=mapping)
        #     pipe.execute()
        """

    def set_multiples(self, key_list: list = None, name_list: list = None, email_list: list = None):
        pipe = {}
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k, n, e in zip(uid(k_list=key_list), name_list, email_list):
            node = self.sharder.get_node_url(shard_key=k)
            pipe[node].hset(k, mapping={'name': n, 'email': e})

        for p in pipe.values():
            p.execute(), p.close()
        """
        if key_list is None:
            raise TypeError('None type passed as argument (mapping=None)')
        # site_key_list = []
        for k, n, e in zip(key_list, name_list, email_list):
            k = 'userID' + ':' + str(k)
            site_id = self.sharder.get_node_url(shard_key=k)
            self.redis_db[site_id].hset(k, mapping={'name': n, 'email': e})
            # self.table.set_site(key=k)
            # site_id = self.table.get_site(key=k)

        """

    def del_fields(self, *, hash_key: int = None, fields: list = None):
        """
        del_fields deletes the fields of the passed key from the database
        :param hash_key: key from the key-value pair
        :param fields: fields from the key to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if hash_key is None or fields is None:
            raise TypeError('None type passed as argument.')

        k = 'userID' + ':' + str(hash_key)
        try:
            site_id = self.sharder.get_node_url(shard_key=k)
            # site_id = self.table.get_site(key=k)
            with self.redis_db[site_id].pipeline() as pipe:
                pipe.watch(k)
                pipe.multi()
                for field in fields:
                    pipe.hdel(k, field)
                pipe.execute()
        except KeyError as err:
            print(k, 'does not exist. Exception:', err)

    def del_keys(self, *, key_list: list = None):
        """
        del_keys deletes all given key list from the database
        :param key_list: key list to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database

         for hash_key in hash_key_list:
            k = 'userID' + ':' + str(hash_key)
            try:
                site_id = self.sharder.get_node_url(shard_key=k)
                # site_id = self.table.get_site(key=k)
                with self.redis_db[site_id].pipeline() as pipe:
                    pipe.watch(k)
                    pipe.multi()
                    pipe.delete(k)
                    pipe.execute()
            except KeyError as err:
                print(k, 'does not exist. Exception:', err)
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

    def get_range(self, *, start: int = 0, end: int):
        """
        res = []
        for i in range(start, end + 1):
            k = 'userID' + ':' + str(i)
            try:
                site_id = self.sharder.get_node_url(shard_key=k)
                hash_values = self.redis_db[site_id].hgetall(k)
                res.append(hash_values)
            except KeyError:
                continue
        return res
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

    def flush_all(self):
        """
        flush_all wipes all data from all database instances
        :return: None
        """
        for db_nodes in self.redis_db.values():
            assert db_nodes.flushdb()

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
    elif len(k_list) == 1:
        return 'userID' + ':' + '{:04d}'.format(k_list[0])
    else:
        return ['userID' + ':' + '{:04d}'.format(k) for k in k_list]
