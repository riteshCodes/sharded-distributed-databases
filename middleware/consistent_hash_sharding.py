import xxhash


class ConsistentHashSharder:
    def __init__(self, num_replicas: int):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []

    def add_node(self, node):
        for i in range(self.num_replicas):
            replica = node + ':' + str(i)
            key = hash_func(replica)
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.num_replicas):
            replica = node + ':' + str(i)
            print(replica)
            key = hash_func(replica)
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None

        hash_key = hash_func(key)
        index = self._get_index(hash_key)
        return self.ring[self.sorted_keys[index]]

    def _get_index(self, key):
        for i, node in enumerate(self.sorted_keys):
            if key <= node:
                return i
        return 0


def hash_func(data: str):
    """
    hash_func generates 64-bit hashes, using vectorized arithmetic. xxHash is an Extremely fast Hash algorithm,
    processing at RAM speed limits
    :param data: input data
    :return: 64-bit hash
    """
    return xxhash.xxh3_64_intdigest(data.encode())


if __name__ == '__main__':
    sharder = ConsistentHashSharder(num_replicas=1)

    # Add some nodes to the sharder
    nodes = ["redis://:sharding-ddms@10.0.2.82:6379/0", "redis://:sharding-ddms@10.0.2.83:6379/0",
             "redis://:sharding-ddms@10.0.2.84:6379/0", "redis://:sharding-ddms@10.0.2.85:6379/0"]

    for node in nodes:
        sharder.add_node(node)

    # Use the sharder to determine which node a key should be stored on
    key = '123'
    node = sharder.get_node(key)
    print(f"Key {key} should be stored on node {node}")
    print(sharder.ring)
    print(sharder.sorted_keys)
    sharder.remove_node('redis://:sharding-ddms@10.0.2.85:6379/0')

    print('test')
    print(sharder.ring)
    print(sharder.sorted_keys)
    node = sharder.get_node(key)
    print(f"Key {key} should be stored on node {node}")
