import grpc
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub

from google.protobuf.json_format import MessageToDict

import numpy as np
import random

from time import perf_counter
import timeit
from time_profiling import write_to_excel_exec_time, write_to_excel_wall_time

HOST = 'localhost'
# HOST = '10.0.2.87'
PORT = '6379'


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
    timeit module measures the execution time of a function.
    It runs the function multiple times (number argument) and returns the average execution time (in seconds)
    :param function: function for time profiling
    :param iterations:
    :return: execution time (in seconds)
    """
    return timeit.timeit(lambda: function, number=iterations)


def latency(*, stub, iterations, u_ids, names, emails):
    """
    timeit module measures the execution time of a function.
    It runs the function multiple times (number argument) and returns the average execution time (in seconds)
    :param stub:
    :param iterations:
    :param u_ids:
    :param names:
    :param emails:
    :return: execution time (in seconds)
    """
    measurements = []
    """
    print(f'Time Profiling (Wall Time/Total Latency), number of iterations = {iterations}')
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        test_connection(stub=stub, message="CONNECTION TEST")
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
        # total_latency = lat / iterations
    total_latency = lat
    # measurements.append(total_latency)

    print(f'Wall time in seconds (test_connection): {total_latency}')
    #  write_to_excel_wall_time(sheet_name='test_connection', data=np.array(measurements))
 """
    # userID=u_ids[random.randint(0, 999)]
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        set_single(stub=stub, userID=u_ids[random.randint(0, 999)], name="single@name", email="single@email")
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (set_single): {total_latency}')
   #  write_to_excel_wall_time(sheet_name='test_connection', data=np.array(measurements))
    """
    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        set_multiples(stub=stub, userIDList=u_ids, nameList=names, emailList=emails)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (set_multiples): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        get_single(stub=stub, key=u_ids[random.randint(0, 999)])
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (get_single): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        get_multiples(stub=stub, k_list=u_ids)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (get_multiples): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        get_range(stub=stub, start=0, end=999)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (get_range): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        del_keys(stub=stub, k_list=[u_ids[random.randint(0, 999)]])
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (del_single_key): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        del_keys(stub=stub, k_list=u_ids)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (del_keys): {total_latency}')

    lat = 0
    for it in range(0, iterations):
        t1_start = perf_counter()  # Start the stopwatch / counter
        get_key_space_info(stub=stub)
        t1_stop = perf_counter()  # Stop the stopwatch / counter
        lat += (t1_stop - t1_start)
    total_latency = lat / iterations
    print(f'Wall time in seconds (key_space_info): {total_latency}')
"""


def run(*, u_ids: list, names: list, emails: list):
    """
    The run method, that sends gRPC conformant messages to the server
    """
    with grpc.insecure_channel(f'{HOST}:6379') as channel:
        stub = CommunicationServiceStub(channel)
        try:
            # Connection Test
            # test_connection(stub=stub, message="CONNECTION TEST")

            # Set values for single key
            # print(set_single(stub=stub, userID=2, name="Ritesh", email="gmail"))

            # Get value from single key
            # print(get_single(stub=stub, key=9))

            # Set values to multiple keys
            # set_multiples(stub=stub, userIDList=u_ids, nameList=names, emailList=emails)
            # set_multiples(stub=stub, userIDList=[0, 1, 2, 3, 4, 5], nameList=['N0', 'N1', 'N2', 'N3', 'N4', 'N5'],
            #              emailList=['E0', 'E1', 'E2', 'E3', 'E4', 'E5'])

            # Get values from multiple keys
            # print(get_multiples(stub=stub, k_list=[9]))

            # Delete entries from given keys
            # del_keys(stub=stub, k_list=[4]

            # Delete entries
            # del_keys(stub=stub, k_list=u_ids)

            # Get values from given range of keys
            # print(get_range(stub=stub, start=0, end=100))

            # Site_Name:Total_Keys mapping
            # keyspace_info = get_key_space_info(stub=stub)
            # print("Total number of keys present in the sites :")
            # print(keyspace_info)

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
            ############################################################################################################

            latency(stub=stub, iterations=1, u_ids=u_ids, names=names, emails=emails)
            # latency(stub=stub, iterations=1000, u_ids=u_ids, names=names, emails=emails)
            # print(execution_time(function=test_connection(stub=stub, message="CONNECTION TEST"), iterations=100))
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            channel.unsubscribe(close)
            exit()


def close(channel):
    """
    Function to close the channel
    :param channel:
    :return:
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
    # stub.getMultiple(KeyList(key_list=[Key(key=1), Key(key=2)]))
    keys = KeyList().key_list
    #

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


if __name__ == "__main__":
    test_user_ids = []
    test_names = []
    test_emails = []
    for i in range(1000):
        test_user_ids.append(i)
        test_names.append(f'N-:{str(i)}')
        test_emails.append(f'@Email-:{str(i)}')

    run(u_ids=test_user_ids, names=test_names, emails=test_emails)
