import random
import redis

# redis/utils.py
try:
    import hiredis  # hiredis as minimalistic C client library for the Redis database

    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False

from config import InfoTable, hash_func

store = {}  # Look-up table (dict type) containing <Hashed_Keys(int)-Redis-URL(str)> pairs for each client


class MWare:
    """
    Mware Class
    """

    def __init__(self, *, client_id: int, site_count: int = 1):
        """
        init
        :param client_id:
        :param site_count: site_count = 1; default number of sites (single site)
        """

        # redis database, config file: /etc/redis/6379.conf

        self.table = InfoTable()
        __table_sites = self.table.sites

        self.redis_db = {}

        for site in __table_sites:
            self.redis_db[site] = redis.StrictRedis(
                connection_pool=redis.ConnectionPool.from_url(site, decode_responses=True))
            # TODO persistence to disk
            for key in self.redis_db[site].scan_iter():
                # store.setdefault(site, []).append(hash_func(data=key))
                store[hash_func(data=key)] = site

        self.table.init_info(data=store)
        self.client_id = client_id

    def get_all(self, *, hash_key_list: list = None):
        """
        get_all retrieves all key-value pairs (data) from the given key_list in the database
        :param hash_key_list: list of keys from which data is fetched
        :return: mapping of the values as dict or KeyError: if the key is not present in the database
        """
        if hash_key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        res = []
        for hash_key in hash_key_list:
            k = 'Client:' + str(self.client_id) + ':' + str(hash_key)

            try:
                site_id = self.table.get_site(key=k)
                hash_values = self.redis_db[site_id].hgetall(k)
                res.append(hash_values)
            except KeyError as err:
                print(k, 'does not exist. Exception:', err)

        return res

    def get_fields(self, *, hash_key: int = None, field_list: list = None):
        """
        get_fields returns all the fields values from the given key in the database
        :param hash_key: key from which data is fetched
        :param field_list: fields of the keys from where data is fetched
        :return:
        """
        if hash_key is None or field_list is None:
            raise TypeError('None type passed as argument')

        k = 'Client:' + str(self.client_id) + ':' + str(hash_key)

        try:
            site_id = self.table.get_site(key=k)
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

        k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
        self.table.set_site(key=k)
        site_id = self.table.get_site(key=k)

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
            k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            self.table.set_site(key=k)
            site_id = self.table.get_site(key=k)
            # site_key_list.append((site_id, k))
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
        """

        """
        if key_list is None:
            raise TypeError('None type passed as argument (mapping=None)')
        # site_key_list = []
        for k, n, e in zip(key_list, name_list, email_list):
            k = 'Client:' + str(self.client_id) + ':' + str(k)
            self.table.set_site(key=k)
            site_id = self.table.get_site(key=k)
            self.redis_db[site_id].hset(k, mapping={'name': n, 'email': e})

    def del_fields(self, *, hash_key: int = None, fields: list = None):
        """
        del_fields deletes the fields of the passed key from the database
        :param hash_key: key from the key-value pair
        :param fields: fields from the key to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if hash_key is None or fields is None:
            raise TypeError('None type passed as argument.')

        k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
        try:
            site_id = self.table.get_site(key=k)
            with self.redis_db[site_id].pipeline() as pipe:
                pipe.watch(k)
                pipe.multi()
                for field in fields:
                    pipe.hdel(k, field)
                pipe.execute()
        except KeyError as err:
            print(k, 'does not exist. Exception:', err)

    def del_keys(self, *, hash_key_list: list = None):
        """
        del_keys deletes all given key list from the database
        :param hash_key_list: key list to delete
        :return: None: if successful, KeyError: if the key to delete is not present in the database
        """
        if hash_key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        for hash_key in hash_key_list:
            k = 'Client:' + str(self.client_id) + ':' + str(hash_key)
            try:
                site_id = self.table.get_site(key=k)
                with self.redis_db[site_id].pipeline() as pipe:
                    pipe.watch(k)
                    pipe.multi()
                    pipe.delete(k)
                    pipe.execute()
            except KeyError as err:
                print(k, 'does not exist. Exception:', err)

    # self.redis_db.delete(*key_list)

    def flush_all(self):
        """
        flush_all wipes all data of all database instances
        :return: None
        """
        for site in self.table.sites:
            self.redis_db[site].flushdb()

    def key_space_inf(self):
        """
        key_space_inf returns the total number of keys present in each site
        :return: key-value pairs (dict) with key as site and value as total number of keys present
        """
        inf = {}
        for site_id in self.table.sites:
            inf[site_id] = self.redis_db[site_id].dbsize()
        return inf


if __name__ == '__main__':
    print("MWare is running")
