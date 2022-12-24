import config
from main import MWare
import sharding
from config import InfoTable

if __name__ == '__main__':
    test = MWare(client_id=1)
    test.set_multiple(hash_key_list=[1, 2, 3], userID=9, location='Germany', role='BUyer')
    print(test.get_all(hash_key_list=[1, 2, 3]))
    print(test.get_fields(hash_key=1, field_list=['userID', 'role', 'location']))
    print(test.key_space_inf())
    test.flush_all()
    # test.set_multiple(hash_key_list=[1, 2, 3], userID=9, location='Germany', role='BUyer')
    # test.del_keys(hash_key_list=[88,100,116,105,118,120,117])
    # test.del_fields(hash_key=500, fields=['userID', 'role'])
    # test.flush_all()
    # hash_key = test.set_to(userID=9, location='NEpal', role='BUyer')
    # print(hash_key)
    # hash_key_t = test.set_to(userID=10, location='Darmstadt', role='Seller')
    # print(hash_key_t)
    # test.del_fields(hash_key=58, fields=('userID', 'location'))
    # test.del_keys(hash_key_list=(115, 243, 58))
    # print(test.get_from(5, 26))
    # print(sharding.jump_sharding(key=10000004524524524522452452424000, num_shards=2))
    # print(sharding.jump_sharding(shard_key=sharding.hash_func(data=b'438731645fghfgfgh'), num_shards=5))

    # test = InfoTable()
    # test.set_site(key="9sd9")
    # print(test.get_site(key="9sd9"))
    # print(config.info)
