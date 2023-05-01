# import redis.asyncio as redis
import aioredis as redis

from configs import DB_NODES, VIRTUAL_NODES
from sharding import ConsistentHashSharder
from logger import log_execution_time

import inspect  # for decorator


class MWare:
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

    async def get_single(self, *, key_list: list = None):
        keys = uid(k_list=key_list)
        node = self.sharder.get_node_url(shard_key=keys[0])
        result = [await self.redis_db[node].hgetall(keys[0])]
        return result

    async def get_multiple(self, *, key_list: list = None):
        result = []
        pipe = {}
        keys = uid(k_list=key_list)

        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            await pipe[node].hgetall(k)

        for p in pipe.values():
            result += await p.execute()
        return result

    async def get_range(self, *, start: int = 0, end: int):
        res = []
        pipe = {}

        keys = uid(k_list=[*range(start, end + 1)])
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            await pipe[node].hgetall(k)

        for p in pipe.values():
            res += await p.execute()

        return res

    async def set_to(self, *, key: int, **mapping):
        if mapping is None:
            raise TypeError('None type passed as argument (mapping=None)')

        k = 'userID' + ':' + '{:04d}'.format(key)
        site_id = self.sharder.get_node_url(shard_key=k)
        await self.redis_db[site_id].hset(k, mapping=mapping)

        return 'OK'

    async def set_multiples(self, key_list: list = None, name_list: list = None, email_list: list = None):
        pipe = {}
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        keys = uid(k_list=key_list)
        for k, n, e in zip(keys, name_list, email_list):
            node = self.sharder.get_node_url(shard_key=k)
            await pipe[node].hset(k, mapping={'name': n, 'email': e})

        for p in pipe.values():
            await p.execute()

        return 'OK'

    async def del_multiple(self, *, key_list: list = None):
        if key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')

        pipe = {}
        keys = uid(k_list=key_list)
        for node, pool in self.redis_db.items():
            pipe[node] = pool.pipeline(transaction=True)

        for k in keys:
            node = self.sharder.get_node_url(shard_key=k)
            await pipe[node].delete(k)

        for p in pipe.values():
            await p.execute()

        return 'OK'

    async def del_single(self, *, key_list: list = None):
        if key_list is None:
            raise TypeError('None type passed as argument (hash_key_list=None)')
        keys = uid(k_list=key_list)

        node = self.sharder.get_node_url(shard_key=keys[0])
        await self.redis_db[node].delete(keys[0])

        return 'OK'


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
