import grpc
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub

from google.protobuf.json_format import MessageToDict

from time import perf_counter
import timeit


def run(*, host_address='localhost', port='6379'):
    """
    The run method, that sends gRPC conformant messages to the server
    """
    # Test data
    u_ids = []
    names = []
    emails = []
    for i in range(1000):
        u_ids.append(i)
        names.append(f'N-:{str(i)}')
        emails.append(f'@Email-:{str(i)}')

    data = {'userID': u_ids, 'name': names, 'email': emails}

    with grpc.insecure_channel(f'{host_address}:{port}') as channel:
        stub = CommunicationServiceStub(channel)
        try:
            # execution_time_request(stub=stub, iterations=1000)
            # latency_request(stub=stub, iterations=1000)

            # execution_time_set(stub=stub, set_function='single', iterations=10, data=data)
            # execution_time_set(stub=stub, set_function='multiple', iterations=10, data=data)

            # latency_set(stub=stub, set_function='single', iterations=10, data=data)
            # latency_set(stub=stub, set_function='multiple', iterations=10, data=data)

            # execution_time_get(stub=stub, get_function='single', iterations=10)
            # execution_time_get(stub=stub, get_function='multiple', iterations=10, keys=u_ids)

            # latency_get(stub=stub, get_function='single', iterations=10, keys=data.get('userID'))
            # latency_get(stub=stub, get_function='multiple', iterations=10, keys=data.get('userID'))
            # latency_get(stub=stub, get_function='range', iterations=10, start=0, end=999)

            latency_del(stub=stub, iterations=10, keys=data.get('userID'))
            """
            # Connection Test
            test_connection(stub=stub, message="CONNECTION TEST")

            # Set values for single key
            assert set_single(stub=stub, userID=0, name="Ritesh", email="Gmail") == 'OK'

            # Get value from single key
            print(get_single(stub=stub, key=9))

            # Set values to multiple keys
            # set_multiples(stub=stub, userIDList=u_ids, nameList=names, emailList=emails)

            # Get values from multiple keys
            print(get_multiples(stub=stub, k_list=[9]))

            # Delete entries from given keys
            del_keys(stub=stub, k_list=[4])

            # Delete entries
            del_keys(stub=stub, k_list=u_ids)

            # Get values from given range of keys
            print(get_range(stub=stub, start=0, end=100))

            # Site_Name:Total_Keys mapping
            keyspace_info = get_key_space_info(stub=stub)
            print("Total number of keys present in the sites :")
            print(keyspace_info)
            """
            ############################################################################################################
            """
            print(f'Time Profiling (Execution Time), number of iterations = {10}')

            # print('test_connection')
            # print(execution_time(function=test_connection(stub=stub, message="CONNECTION TEST"), iterations=10))

            print('get_key_space_info')
            print(execution_time(function=get_key_space_info(stub=stub), iterations=10))

            print('set_single')
            print(execution_time(function=set_single(stub=stub, userID=1, name="single@name", email="single@email"),
                                 iterations=10))

            print('set_multiples')
            print(execution_time(function=set_multiples(stub=stub, userIDList=u_ids, nameList=names, emailList=emails),
                                 iterations=10))

            print('get_single')
            print(execution_time(function=get_multiples(stub=stub, k_list=[u_ids[random.randint(0, 999)]]), iterations=10))

            print('get_multiples')
            print(execution_time(function=get_multiples(stub=stub, k_list=u_ids), iterations=10))

            print('get_range')
            print(execution_time(function=get_range(stub=stub, start=0, end=999), iterations=10))

            print('del_single_key')
            print(execution_time(function=del_keys(stub=stub, k_list=[u_ids[random.randint(0, 999)]]), iterations=10))

            print('del_multiples')
            print(execution_time(function=del_keys(stub=stub, k_list=u_ids), iterations=10))
            """
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            channel.unsubscribe(close)
            exit()


def close(channel):
    """
    Function to close the given channel
    """
    channel.close()


def test_connection(*, stub, message):
    # create a valid request message
    print(stub.testConnection(StringMessage(message=message)))


def get_key_space_info(*, stub):
    return parse_to_dict(stub.getKeySpaceInfo(Empty()))


def get_single(*, stub, key):
    proto_data = stub.getSingle(Key(key=key))
    dict_data = MessageToDict(proto_data)
    return dict_data


def get_multiples(*, stub, k_list: list = None):
    keys = KeyList().key_list

    for k in k_list:
        keys.append(Key(key=k))

    proto_data = stub.getMultiple(KeyList(key_list=keys))

    dict_data = MessageToDict(proto_data)
    if isinstance(proto_data, GetDictData):
        return dict_data['getdata']


def get_range(*, stub, start: int, end: int):
    return MessageToDict(stub.getRange(Range(start=start, end=end)))['getdata']


def set_single(*, stub, **mapping):
    return stub.setSingle(Data(userID=mapping.get('userID'), name=mapping.get('name'), email=mapping.get('email')))


def set_multiples(*, stub, **mapping):
    dict_data = Dict().data
    for i, j, k in zip(mapping.get('userIDList'), mapping.get('nameList'), mapping.get('emailList')):
        dict_data.append(Data(userID=i, name=j, email=k))

    stub.setMultiple(Dict(data=dict_data))


def del_keys(*, stub, k_list: list = None):
    keys = KeyList().key_list

    for k in k_list:
        keys.append(Key(key=k))

    return stub.delKeys(KeyList(key_list=keys))


def parse_to_dict(proto_data):
    """
    single values
    """
    dict_data = MessageToDict(proto_data)
    if isinstance(proto_data, MapStringInt) or isinstance(proto_data, MapIntString) or isinstance(proto_data,
                                                                                                  MapDefault):
        return dict_data['keyValue']
    else:
        return dict_data['data']


def parse_to_dict_list(proto_data):
    dict_data = MessageToDict(proto_data)
    if isinstance(proto_data, GetDictData):
        return dict_data['getdata']


def execution_time(*, function, iterations):
    """
        timeit module measures the execution time of a function and returns a single floating point value representing
        the cumulative amount of time spent running the main statement.
        :param function: function for time profiling
        :param iterations:
        :return: execution time (in seconds)
        """
    return timeit.timeit(lambda: function, number=iterations)


def execution_time_request(*, stub, iterations):
    total_exec = execution_time(function=test_connection(stub=stub, message='TEST'),
                                iterations=iterations)
    print(f'Execution time in seconds for {iterations} request : {total_exec}')


def execution_time_set(*, stub, set_function, iterations, data):
    total_exec = 0
    if set_function == 'single':
        total_exec = execution_time(function=set_single(stub=stub,
                                                        userID=data['userID'][0], name=data['name'][0],
                                                        email=data['email'][0]),
                                    iterations=iterations) / iterations

    elif set_function == 'multiple':
        total_exec = execution_time(function=
                                    set_multiples(stub=stub,
                                                  userIDList=data['userID'], nameList=data['name'],
                                                  emailList=data['email']),
                                    iterations=iterations) / iterations
    else:
        print(f'{set_function} : function not defined')

    total_keys = len(data['userID'])
    print(f'Execution time in seconds for setting {total_keys} key-value pairs :: {total_exec}')

    return total_exec

    # return timeit.timeit(lambda: function, number=iterations)


def execution_time_get(*, stub, get_function, iterations, keys=None, start=0, end=0):
    """
    timeit module measures the execution time of a function.
    It runs the function multiple times (number argument) and returns the average execution time (in seconds)
    :param stub:
    :param get_function: function for time profiling
    :param iterations:
    :param keys:
    :param start:
    :param end:
    :return: execution time (in seconds)
    """
    total_exec = 0
    total_keys = 1 if keys is None else len(keys)
    if get_function == 'single':
        total_exec = execution_time(function=
                                    get_single(stub=stub, key=1),
                                    iterations=iterations) / iterations

    elif get_function == 'multiple':
        total_exec = execution_time(function=
                                    get_multiples(stub=stub, k_list=keys),
                                    iterations=iterations) / iterations
    elif get_function == 'range':
        total_exec = execution_time(function=
                                    get_range(stub=stub, start=start, end=end),
                                    iterations=iterations) / iterations
    else:
        print(f'{get_function} : function not defined')

    print(f'Execution time in seconds for getting {total_keys} key-value pairs :: {total_exec}')

    return total_exec


def execution_time_del(*, stub, iterations, keys=None):
    """
    timeit module measures the execution time of a function.
    It runs the function multiple times (number argument) and returns the average execution time (in seconds)
    :param stub:
    :param iterations:
    :param keys:
    :return: execution time (in seconds)
    """
    total_exec = execution_time(function=
                                del_keys(stub=stub, k_list=keys),
                                iterations=iterations) / iterations
    print(f'Execution time in seconds for deleting {len(keys)} key-value pairs :: {total_exec}')
    return total_exec


def latency_request(*, stub, iterations):
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        test_connection(stub=stub, message='TEST')
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    print(f'Latency in seconds for {iterations} request : {lat}')
    return lat


def latency_set(*, stub, set_function, iterations, data: list):
    lat = 0
    total_latency = 0
    if set_function == 'single':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            set_single(stub=stub, userID=data['userID'][0], name=data['name'][0], email=data['email'][0])
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif set_function == 'multiple':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            set_multiples(stub=stub, userIDList=data['userID'], nameList=data['name'], emailList=data['email'])
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    else:
        print(f'{set_function} : function not defined')

    total_keys = len(data['userID'])
    print(f'Wall time in seconds for setting {total_keys} key-value pairs :: {total_latency}')
    return total_latency


def latency_get(*, stub, get_function, iterations, keys=None, start=0, end=0):
    lat = 0
    total_latency = 0
    if get_function == 'single':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            get_single(stub=stub, key=keys[0])
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif get_function == 'multiple':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            get_multiples(stub=stub, k_list=keys)
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    elif get_function == 'range':
        for it in range(0, iterations):
            t1_start = perf_counter()  # Start the stopwatch / counter
            get_range(stub=stub, start=start, end=end)
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            lat += (t1_stop - t1_start)
        total_latency = lat / iterations

    else:
        print(f'{get_function} : function not defined')

    total_keys = len(keys) if keys is not None else (start + end + 1)
    print(f'Wall time in seconds for getting {total_keys} key-value pairs : {total_latency}')
    return total_latency


def latency_del(*, stub, iterations, keys=None):
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        del_keys(stub=stub, k_list=keys)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (del_keys for deleting {len(keys)} keys: {total_latency}')
    return total_latency


if __name__ == "__main__":
    run(host_address='10.0.2.87')
