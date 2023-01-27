import xxhash

from configs import SITES


class ConsistentHashSharder:
    """
    Clockwise ring assignment
    """

    def __init__(self, *, num_replicas: int):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []  # sort the keys in ascending order to place them in the ring

    def add_site(self, *, site_name: str):
        """
        :param site_name:
        """
        for i in range(self.num_replicas):
            replica = site_name + ':' + str(i)
            k = hash_func(data=replica) % 360
            self.ring[k] = site_name
            self.sorted_keys.append(k)
        self.sorted_keys.sort()

    def remove_site(self, *, site_name: str):
        """
        :param site_name:
        """
        for i in range(self.num_replicas):
            replica = site_name + ':' + str(i)
            k = hash_func(data=replica) % 360
            del self.ring[k]
            self.sorted_keys.remove(k)

    def get_node(self, *, k):
        """
        :param k:
        """
        if not self.ring:
            return None

        hash_key = hash_func(data=k) % 360
        index = self._get_index(k=hash_key)
        return self.ring[self.sorted_keys[index]]

    def _get_index(self, *, k):
        """
        :param k:
        """
        for i, site_hash in enumerate(self.sorted_keys):
            if k <= site_hash:
                return i

        return 0  # TODO what if k > site_hash (in total list)
        # Approach: % total sites (without replicas)
        # return self._get_index(k=k % len(SITES))


def hash_func(*, data: str):
    """
    hash_func generates 64-bit hashes, using vectorized arithmetic. xxHash is an Extremely fast Hash algorithm,
    processing at RAM speed limits
    :param data: input data
    :return: 64-bit hash
    """
    return xxhash.xxh3_64_intdigest(data.encode())


def binary_search(array, key):
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = int((low + high) / 2)
        if array[mid] < key:
            low = mid + 1
        elif array[mid] > key:
            high = mid - 1
        else:
            return mid
    return None


if __name__ == '__main__':

    sharder = ConsistentHashSharder(num_replicas=1)

    # Add some nodes to the sharder
    sites = ["redis://:sharding-ddms@10.0.2.82:6379/0", "redis://:sharding-ddms@10.0.2.83:6379/0",
             "redis://:sharding-ddms@10.0.2.84:6379/0", "redis://:sharding-ddms@10.0.2.85:6379/0"]

    for site in sites:
        sharder.add_site(site_name=site)

    # Use the sharder to determine which site a key should be stored on
    key = '789111'
    s = sharder.get_node(k=key)
    print(f"Key {key} should be stored on :  {s}")
    print(sharder.ring)
    print(sharder.sorted_keys)

    sharder.remove_site(site_name='redis://:sharding-ddms@10.0.2.83:6379/0')
    t = sharder.get_node(k=key)
    print(f"Key {key} should be stored on :  {t}")
    print(sharder.ring)
    print(sharder.sorted_keys)

    sharder.remove_site(site_name='redis://:sharding-ddms@10.0.2.85:6379/0')
    u = sharder.get_node(k=key)
    print(f"Key {key} should be stored on :  {u}")
    print(sharder.ring)
    print(sharder.sorted_keys)
