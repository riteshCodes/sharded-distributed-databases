import random
from main import MWare

if __name__ == '__main__':
    # for i in range(0, 10):
    test_data = MWare(client_id=0)
    # set single key store
    test_data.set_to(hash_key=random.randint(0, 20), userID=random.randint(0, 30), name="Something",
                     country="Germany")
    # set multiple key stores
    test_data.set_multiple(hash_key_list=[random.randint(21, 51), random.randint(52, 82), random.randint(83, 113)],
                           userID=777, name='Multiple Assignment', country='Nepal')
    # get all key stores info (server:number-of-values)
    print(test_data.key_space_inf())
    print(test_data.get_all(hash_key_list=[54]))
    print(test_data.get_fields(hash_key=54, field_list=['userID', 'name']))
    test_data.flush_all()
    # flush all data
    # test_data.flush_all()
