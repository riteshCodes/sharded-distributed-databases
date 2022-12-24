import math
import random


def jump_sharding(*, shard_key: int, num_shards: int):
    """
    jump_sharding implements jump consistent hash
    :param shard_key:
    :param num_shards:
    :return:
    """
    if num_shards <= 0:
        raise ValueError("Number of shards must be greater than 0")

    random.seed(shard_key)
    # shard will track jump_sharding(key, j+1)
    shard = -1  # shard number before the previous jump
    j = 0  # shard number before the current jump
    while j < num_shards:
        shard = j
        j = math.floor((shard + 1) / random.random())

    return shard
