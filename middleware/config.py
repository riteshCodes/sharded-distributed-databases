import xxhash

import sharding


def hash_func(*, data: bytes):
    """
    hash_func generates 64-bit hashes, using vectorized arithmetic. xxHash is an Extremely fast Hash algorithm,
    processing at RAM speed limits
    :param data: input data
    :return: 64-bit hash
    """
    return xxhash.xxh3_64_intdigest(data)


class InfoTable:
    """
    InfoTable
    """
    info = {}  # Look-up table (dict type) containing <Hashed_Keys(int)-Redis-URL(str)> pairs

    def __init__(self):
        # self.sites = ["redis://localhost:6379/0", "redis://localhost:6380/0"]
        # Precondition: all the servers must be up and running redis
        # Redis server v=6.0.16
        # self.sites = ["redis://10.0.2.82:6379/0", "redis://10.0.2.83:6379/0"]
        self.sites = ["redis://:sharding-ddms@10.0.2.82:6379/0", "redis://:sharding-ddms@10.0.2.83:6379/0",
                      "redis://:sharding-ddms@10.0.2.84:6379/0", "redis://:sharding-ddms@10.0.2.85:6379/0"]

    @staticmethod
    def init_info(*, data: dict):
        InfoTable.info = data

    def get_site(self, *, key: str):
        """
        get_site
        :param key:
        :return:
        """
        hash_key = hash_func(data=key.encode())
        # return self.info[hash_key]
        if hash_key in self.info.keys():
            return self.info[hash_key]
        else:
            raise KeyError("KeyError")

    def set_site(self, *, key: str):
        """
        set_site
        :param key:
        :return:
        """
        hash_key = hash_func(data=key.encode())
        site_index = sharding.jump_sharding(shard_key=hash_key, num_shards=len(self.sites))
        self.info[hash_key] = self.sites[site_index]
