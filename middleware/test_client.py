from main import MWare
import sharding

if __name__ == '__main__':
    # test = MWare(client_id=1)
    # hash_key = test.set_to(userID=9, location='UPDATE FRA', role='TEST')
    # print(hash_key)
    # test.del_fields(hash_key=58, fields=('userID', 'location'))
    # test.del_keys(hash_key_list=(115, 243, 58))
    # print(test.get_from(5, 26))
    print(sharding.jump_sharding(key=10000004524524524522452452424000, num_shards=2))
    print(sharding.hash_function())
