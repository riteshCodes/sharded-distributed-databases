import grpc
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub

from google.protobuf.json_format import MessageToDict

from time import perf_counter
import timeit

HOST = 'localhost'
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


def execution_time(*, function):
    """
    timeit module measures the execution time of a function.
    It runs the function multiple times (number argument) and returns the average execution time (in seconds)
    :param function: function for time profiling
    :return: execution time (in seconds)
    """
    return timeit.timeit(lambda: function, number=1)


def run(*, u_ids: list, names: list, emails: list):
    """
    The run method, that sends gRPC conformant messages to the server
    """
    with grpc.insecure_channel("localhost:6379") as channel:
        stub = CommunicationServiceStub(channel)
        try:
            # Connection Test
            test_connection(stub=stub, message="CONNECTION TEST")

            # Set values for single key
            # print(set_single(stub=stub, userID=2, name="Ritesh", email="gmail"))

            # Get value from single key
            # print(get_single(stub=stub, key=9))

            # Set values to multiple keys
            set_multiples(stub=stub, userIDList=u_ids, nameList=names, emailList=emails)
            # set_multiples(stub=stub, userIDList=[0, 1, 2, 3, 4, 5], nameList=['N0', 'N1', 'N2', 'N3', 'N4', 'N5'],
            #              emailList=['E0', 'E1', 'E2', 'E3', 'E4', 'E5'])

            # Get values from multiple keys
            # print(get_multiples(stub=stub, k_list=[9]))

            # Delete entries from given keys
            # del_keys(stub=stub, k_list=[4])

            # Get values from given range of keys
            print(get_range(stub=stub, start=0, end=100))

            # Site_Name:Total_Keys mapping
            keyspace_info = get_key_space_info(stub=stub)
            print("Total number of keys present in the sites :")
            print(keyspace_info)

            ############################################################################################################
            print('Time Profiling (Execution Time)')

            print(execution_time(function=get_key_space_info(stub=stub)))

            ############################################################################################################
            print('Time Profiling (Wall Time)')
            t1_start = perf_counter()  # Start the stopwatch / counter
            get_key_space_info(stub=stub)
            t1_stop = perf_counter()  # Stop the stopwatch / counter
            print(f'Wall time in seconds: {t1_stop - t1_start}')

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
