from main import RedisClient
from time import perf_counter
import timeit

client = RedisClient()


def execution_time(*, function, iterations):
    return timeit.timeit(lambda: function, number=iterations)


def execution_time_set(*, set_function, iterations, data):
    total_exec = 0
    if set_function == 'single':
        total_exec = execution_time(function=client.set_to(key=data['userID'][0], name=data['name'][0],
                                                           email=data['email'][0]),
                                    iterations=iterations) / iterations

    elif set_function == 'multiple':
        total_exec = execution_time(function=client.set_multiples(key_list=data['userID'], name_list=data['name'],
                                                                  email_list=data['email']),
                                    iterations=iterations) / iterations
    else:
        print(f'{set_function} : function not defined')

    total_keys = len(data['userID'])
    print(f'Execution time in seconds for setting {total_keys} key-value pairs :: {total_exec}')

    return total_exec


def execution_time_get(*, get_function, iterations, keys=None, start=0, end=0):
    total_exec = 0

    if get_function == 'single':
        total_exec = execution_time(function=
                                    client.get_all(key_list=[keys[0]]),
                                    iterations=iterations) / iterations

    elif get_function == 'multiple':
        total_exec = execution_time(function=
                                    client.get_all(key_list=keys),
                                    iterations=iterations) / iterations
    elif get_function == 'range':
        total_exec = execution_time(function=
                                    client.get_range(start=start, end=end),
                                    iterations=iterations) / iterations
    else:
        print(f'{get_function} : function not defined')
    total_keys = len(range(start, end + 1)) if get_function == 'range' else len(keys)
    print(f'Execution time in seconds for getting {total_keys} key-value pairs :: {total_exec}')

    return total_exec


def execution_time_del(*, iterations, keys=None):
    total_exec = execution_time(function=
                                client.del_keys(key_list=keys),
                                iterations=iterations) / iterations
    print(f'Execution time in seconds for deleting {len(keys)} key-value pairs :: {total_exec}')
    return total_exec


def latency_ping(*, iterations, ping_calls):
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        for _ in range(ping_calls):
            client.ping()
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)

    total_latency = lat / iterations
    print(f'Wall time in pinging redis key-value store {iterations} times : {total_latency}')
    return total_latency


def latency_set(*, set_function, iterations, data: list):
    lat = 0
    total_latency = 0
    if set_function == 'single':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            client.set_to(key=data['userID'][0], name=data['name'][0],
                          email=data['email'][0]),
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif set_function == 'multiple':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            client.set_multiples(key_list=data['userID'], name_list=data['name'],
                                 email_list=data['email']),
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    else:
        print(f'{set_function} : function not defined')

    total_keys = len(data['userID'])
    print(f'Wall time in seconds for setting {total_keys} key-value pairs :: {total_latency}')
    return total_latency


def latency_get(*, get_function, iterations, keys=None, start=0, end=0):
    lat = 0
    total_latency = 0
    if get_function == 'single':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            client.get_all(key_list=[keys[0]]),
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif get_function == 'multiple':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            client.get_all(key_list=keys),
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif get_function == 'range':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            client.get_range(start=start, end=end)
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    else:
        print(f'{get_function} : function not defined')
    total_keys = len(range(start, end + 1)) if get_function == 'range' else len(keys)
    print(f'Wall time in seconds for getting {total_keys} key-value pairs : {total_latency}')
    return total_latency


def latency_del(*, iterations, keys=None):
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        client.del_keys(key_list=keys)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (del_keys for deleting {len(keys)} keys: {total_latency}')
    return total_latency


if __name__ == '__main__':
    # Test data
    u_ids = []
    names = []
    emails = []
    for i in range(10):
        u_ids.append(i)
        names.append(f'N-:{str(i)}')
        emails.append(f'@Email-:{str(i)}')

    test_data = {'userID': u_ids, 'name': names, 'email': emails}

    ###################################################################################################################
    # Test
    # latency_ping(iterations=10, ping_calls=1000)

    # execution_time_set(set_function='single', iterations=10, data=test_data)
    # execution_time_set(set_function='multiple', iterations=10, data=test_data)
    # latency_set(set_function='single', iterations=10, data=test_data)
    # latency_set(set_function='multiple', iterations=10, data=test_data)

    # execution_time_get(get_function='single', iterations=10, keys=u_ids)
    # execution_time_get(get_function='multiple', iterations=10, keys=u_ids)
    # latency_get(get_function='single', iterations=10, keys=u_ids)
    # latency_get(get_function='multiple', iterations=10, keys=u_ids)

    # execution_time_get(get_function='range', iterations=10, start=0, end=len(u_ids) - 1)
    latency_get(get_function='range', iterations=10, start=0, end=len(u_ids) - 1)

    # execution_time_del(iterations=10, keys=[test_data['userID'][0]])
    # latency_del(iterations=10, keys=test_data['userID'])
