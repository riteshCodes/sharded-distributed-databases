import math
import random


def crc_16(data: bytes, poly=0x8408):
    """
    CRC-16-CCITT Algorithm
    """
    data = bytearray(data)
    crc = 0xFFFF
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)

    return crc & 0xFFFF


def jump_sharding(*, key: int, num_shards: int):
    random.seed(key)
    # shard will track jump_sharding(key, j+1)
    shard = -1  # shard number before the previous jump
    j = 0  # shard number before the current jump
    while j < num_shards:
        shard = j
        j = math.floor((shard + 1) / random.random())

    return shard
