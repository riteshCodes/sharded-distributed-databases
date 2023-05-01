import random
import time

from optimized_operations import RedisClient
import utils

direct_client = RedisClient()
large_content = utils.read_data(data_code=1000)
small_content = utils.read_data(data_code=100)


def response_time_get(*, get_function, iterations):
    res = 0
    total_response_time = 0
    if get_function == 'single':
        for it in range(0, iterations):
            key_list = random.sample(list(small_content['userID']),
                                     1)  # Get 1 random key to set/update from the content

            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.get_all(key_list=key_list)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    elif get_function == 'multiple':
        for it in range(0, iterations):
            key_list = large_content['userID']

            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.get_all(key_list=key_list)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    elif get_function == 'range':
        for it in range(0, iterations):
            start = random.randint(0, 999)
            end = start + 100  # range of 100 keys
            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.get_range(start=start, end=end)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    else:
        print(f'{get_function} : function not defined')

    print(f'Response time in ms for get_{get_function}: {total_response_time}')
    return total_response_time


def response_time_set(*, set_function, iterations):
    res = 0
    total_response_time = 0
    if set_function == 'single':
        for it in range(0, iterations):
            key = random.randint(0, 999)  # Random key-generation
            mapping = {'name': 'single_test', 'email': 'single_test'}
            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.set_to(key=key, mapping=mapping)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    elif set_function == 'multiple':
        for it in range(0, iterations):
            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.set_multiples(key_list=large_content['userID'], name_list=large_content['name'],
                                        email_list=large_content['email'])
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    else:
        print(f'{set_function} : function not defined')

    print(f'Response time in ms for set_{set_function} : {total_response_time}')
    return total_response_time


def response_time_del(*, del_function, iterations):
    res = 0
    total_response_time = 0
    if del_function == 'single':
        for it in range(0, iterations):
            key_list = random.sample(range(0, 999), 1)  # Generate 1 random key
            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.del_keys(key_list=key_list)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    elif del_function == 'multiple':
        for it in range(0, iterations):
            key_list = random.sample(range(0, 999), 100)  # Generate 100 random keys
            t1_start = time.time()  # Start the stopwatch / counter
            direct_client.del_keys(key_list=key_list)
            t1_stop = time.time()  # Stop the stopwatch / counter
            res += (t1_stop - t1_start) * 1000
        total_response_time = res / iterations

    else:
        print(f'{del_function} : function not defined')

    print(f'Response time in ms for del_{del_function} : {total_response_time}')
    return total_response_time


if __name__ == '__main__':
    response_time_set(set_function='single', iterations=10)
    response_time_set(set_function='multiple', iterations=10)
    response_time_get(get_function='single', iterations=10)
    response_time_get(get_function='multiple', iterations=10)
    response_time_get(get_function='range', iterations=10)
    response_time_del(del_function='single', iterations=10)
    response_time_del(del_function='multiple', iterations=10)
