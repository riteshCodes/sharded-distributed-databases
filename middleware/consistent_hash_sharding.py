import hashlib


class ConsistentHashSharder:
    def __init__(self, num_replicas=100):
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []

    def add_node(self, node):
        for i in range(self.num_replicas):
            replica = node + ':' + str(i)
            key = self._hash(replica)
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        for i in range(self.num_replicas):
            replica = node + ':' + str(i)
            key = self._hash(replica)
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key):
        if not self.ring:
            return None

        hash_key = self._hash(key)
        index = self._get_index(hash_key)
        return self.ring[self.sorted_keys[index]]

    def _get_index(self, key):
        for i, node in enumerate(self.sorted_keys):
            if key <= node:
                return i
        return 0

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
