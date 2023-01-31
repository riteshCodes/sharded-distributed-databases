import xxhash
from farmhash import FarmHash64
from math import floor


class ConsistentHashSharder:
    """
    Clockwise ring assignment
    """

    def __init__(self, *, virtual_sites_count: int):
        self.virtual_sites_count = virtual_sites_count
        self.ring = {}
        self.sorted_keys = []  # sort the keys in ascending order to place them in the ring

    def add_site(self, *, site_name: str):
        """
        :param site_name:
        """
        for i in range(self.virtual_sites_count):
            virtual_site = site_name + ':' + str(i)
            k = hash_func(func_type='farmhash', data=virtual_site) % 360

            self.ring[k] = site_name
            self.sorted_keys.append(k)

        self.sorted_keys.sort()

    def remove_site(self, *, site_name: str):
        """
        :param site_name:
        """
        for i in range(self.virtual_sites_count):
            virtual_site = site_name + ':' + str(i)
            k = hash_func(func_type='farmhash', data=virtual_site) % 360

            del self.ring[k]
            self.sorted_keys.remove(k)

    def get_site(self, *, shard_key):
        """
        :param shard_key:
        """
        if not self.ring:
            return None

        # hash_key = hash_func(func_type='xxhash', data=shard_key) % 360
        hash_key = hash_func(func_type='farmhash', data=shard_key) % 360
        index = self._get_index(k=hash_key)
        return self.ring[self.sorted_keys[index]]

    def _get_index(self, *, k):
        """
        TODO Efficient Search
        :param k:
        """
        for i, site_hash in enumerate(self.sorted_keys):
            if k <= site_hash:
                return i

        return 0  # After the last search, go to first site


def hash_func(*, func_type: str, data: str):
    """
    hash_func generates 64-bit hashes, using vectorized arithmetic. xxHash is an Extremely fast Hash algorithm,
    processing at RAM speed limits
    :param func_type: xxhash or farmhash
    :param data: input data
    :return: 64-bit hash
    """
    if func_type == 'xxhash':
        return xxhash.xxh3_64_intdigest(data.encode())
    if func_type == 'farmhash':
        return FarmHash64(data)

    return TypeError('Hash function type error')


def binary_search(array, key):
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = floor((low + high) / 2)
        if array[mid] < key:
            low = mid + 1
        elif array[mid] > key:
            high = mid - 1
        else:
            return mid
    return None


if __name__ == '__main__':
    sharder = ConsistentHashSharder(virtual_sites_count=5)

    # Add some nodes to the sharder
    # sites = ["redis://:sharding-ddms@10.0.2.82:6379/0", "redis://:sharding-ddms@10.0.2.83:6379/0","redis://:sharding-ddms@10.0.2.84:6379/0", "redis://:sharding-ddms@10.0.2.85:6379/0"]
    sites = ['n1', 'n2', 'n3', 'n4', 'n5']

    for site in sites:
        sharder.add_site(site_name=site)

    # Use the sharder to determine which site a key should be stored on
    key = '789111'
    s = sharder.get_site(shard_key=key)
    print(f"Key {key} should be stored on :  {s}")
    print(sharder.ring)
    print(sharder.sorted_keys)

    sharder.remove_site(site_name='n3')
    t = sharder.get_site(shard_key=key)
    print(f"Key {key} should be stored on :  {t}")
    print(sharder.ring)
    print(sharder.sorted_keys)


