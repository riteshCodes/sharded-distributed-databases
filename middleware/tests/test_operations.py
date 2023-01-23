import random
from main import MWare

if __name__ == '__main__':
    test_data = MWare(client_id=0)

    # test_data.flush_all()

    test_data.set_multiples(key_list=[0, 1, 2, 3, 4, 5], name_list=['N0', 'N1', 'N2', 'N3', 'N4', 'N5'],
                            email_list=['E0', 'E1', 'E2', 'E3', 'E4', 'E5'])

    for i in range(0, 20):
        # set single key-value pair (value as mapping)
        test_data.set_to(hash_key=random.randint(0, 20), name="name" + str(random.randint(0, 50)),
                         email="email" + str(random.randint(51, 100)))

    # Get values from range of keys
    ranges = test_data.get_range(start=0, end=10)
    print(ranges)
    print(len(ranges))

    # Get all values from given keys
    values = test_data.get_all(hash_key_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(values)
    print(len(values))

    non_existing_key = test_data.get_all(hash_key_list=[99])
    print(non_existing_key)

    single_key = test_data.get_all(hash_key_list=[10])
    print(single_key)

    field_values = test_data.get_fields(hash_key=10, field_list=['name', 'email'])
    print(field_values)

    # get all key stores info (server:number-of-values)
    print(test_data.key_space_inf())
    # test_data.flush_all()
