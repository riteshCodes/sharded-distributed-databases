from farmhash import FarmHash32


class ConsistentHashSharder:
    """
    Clockwise ring assignment of given keys to nodes
    """

    def __init__(self, *, virtual_nodes: int):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []  # sort the keys in ascending order to place them in the ring

    def add_node(self, *, node_url: str):
        """
        :param node_url:
        """
        for i in range(self.virtual_nodes):
            v_node = node_url + ':' + str(i)
            k = hash_func(data=v_node) % 4294967295

            self.ring[k] = node_url
            self.sorted_keys.append(k)

        self.sorted_keys.sort()

    def remove_node(self, *, node_url: str):
        """
        :param node_url:
        """
        for i in range(self.virtual_nodes):
            v_node = node_url + ':' + str(i)
            k = hash_func(data=v_node) % 4294967295
            del self.ring[k]
            self.sorted_keys.remove(k)

    def get_node_url(self, *, shard_key):
        """
        :param shard_key:
        """
        if not self.ring:
            return None

        k = hash_func(data=shard_key) % 4294967295
        index = _get_index(array=self.sorted_keys, value=k)
        return self.ring[self.sorted_keys[index]]


def hash_func(*, data: str):
    """
    hash_func generates 64-bit hash digest for string data, using vectorized arithmetic. xxHash is an Extremely fast Hash algorithm,
    processing at RAM speed limits (pip install cityhash)
    :param data: input data
    :return: 64-bit hash
    """
    return FarmHash32(data)


def _get_index(*, array, value):
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if array[mid] < value:
            low = mid + 1
        else:
            high = mid - 1
    return low if low < len(array) else 0
