import grpc
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub

from google.protobuf.json_format import MessageToDict

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


def run():
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

            # Set (same) values to multiple keys
            # set_multiples(stub=stub, userIDList=[0, 1, 2, 3, 4, 5], nameList=['N0', 'N1', 'N2', 'N3', 'N4', 'N5'],
            #              emailList=['E0', 'E1', 'E2', 'E3', 'E4', 'E5'])

            # Get values from multiple keys
            # print(get_multiples(stub=stub, k_list=[9]))

            # Delete entries from given keys
            # del_keys(stub=stub, k_list=[4])

            # Site_Name:Total_Keys mapping
            keyspace_info = get_key_space_info(stub=stub)
            # print("Total number of keys present in the sites :")
            print(keyspace_info)

        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            channel.unsubscribe(close)
            exit()


def close(channel):
    """
    Close the channel
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
    pass


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
    run()
