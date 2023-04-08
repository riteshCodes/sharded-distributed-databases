from farmhash import FarmHash32
import hashlib

import bisect

MAX_NUMBER_32_BITS = 4294967295
# 16-bits binary value can represent 2^16 distinct values
MAX_NUMBER_16_BITS = 65535  # Range of hash values used: [0, (2^16 -1)]


class ConsistentHashSharder:
    """
    Clockwise ring assignment of given keys to nodes
    """

    def __init__(self, *, virtual_nodes: int):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.sorted_keys = []  # sort the keys in ascending order to place them in the ring

    def add_node(self, *, node_url: str):
        if self.virtual_nodes != 0:
            for i in range(self.virtual_nodes):
                v_node = node_url + ':' + str(i)

                k = hash_md5(data=v_node) % MAX_NUMBER_16_BITS
                # k = hash_md5(data=v_node) % MAX_NUMBER_32_BITS

                self.ring[k] = node_url
                self.sorted_keys.append(k)
        else:
            k = hash_md5(data=node_url + ':' + '0') % MAX_NUMBER_16_BITS
            # k = hash_md5(data=node_url + ':' + '0') % MAX_NUMBER_32_BITS

            self.ring[k] = node_url
            self.sorted_keys.append(k)

        self.sorted_keys.sort()

    def remove_node(self, *, node_url: str):
        for i in range(self.virtual_nodes):
            v_node = node_url + ':' + str(i)

            k = hash_md5(data=v_node) % MAX_NUMBER_16_BITS
            # k = hash_md5(data=v_node) % MAX_NUMBER_32_BITS

            del self.ring[k]
            self.sorted_keys.remove(k)

    def get_node_url(self, *, shard_key):
        if not self.ring:
            return None

        k = hash_md5(data=shard_key) % MAX_NUMBER_16_BITS
        # k = hash_md5(data=shard_key) % MAX_NUMBER_32_BITS

        index = _get_index(array=self.sorted_keys, value=k)
        return self.ring[self.sorted_keys[index]]


def hash_func(*, data: str):
    """
    hash_func generates 64-bit hash digest for string data, using vectorized arithmetic. xxHash is an Extremely fast
    Hash algorithm, processing at RAM speed limits (pip install cityhash)
    :param data: input data
    :return: 64-bit hash
    """
    return FarmHash32(data)


def hash_md5(*, data: str):
    h_object = hashlib.md5(data.encode())
    digest_32 = h_object.hexdigest()  # 32 character hexadecimal (128-bits hash value)
    digest_8 = digest_32[:8]  # Truncated to 8 characters hexadecimal (32-bits hash value), 4 byte
    # digest_4 = digest_32[:4]  # Truncated to 4 characters hexadecimal (16-bits hash value), 2 byte
    return int(digest_8, 16)


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


def find_next_position(*, sorted_array, target):
    index = bisect.bisect(sorted_array, target)
    return index
