import random

from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub
from locust import task

from google.protobuf.json_format import MessageToDict

import base_client, utils


class BenchmarkingClient(base_client.BaseUser):
    host = '10.0.2.87:6379'  # middleware address
    stub_class = CommunicationServiceStub

    @task
    def ping(self):
        self.stub.testConnection(StringMessage(message='Ping Load Testing'))

    @task
    def get_single(self):
        data = self.stub.getSingle(Key(key=random.randint(0, 99)))
        dict_data = MessageToDict(data)
        return dict_data

    @task
    def get_multiples(self, data_code: int = 100):
        keys = KeyList().key_list

        for k in utils.read_data(data_code=data_code)['userID']:
            keys.append(Key(key=k))

        proto_data = self.stub.getMultiple(KeyList(key_list=keys))

        dict_data = MessageToDict(proto_data)
        if isinstance(proto_data, GetDictData):
            return dict_data['getdata']

    @task
    def get_range(self, start: int = 0, end: int = random.randint(0, 99)):
        return MessageToDict(self.stub.getRange(Range(start=start, end=end)))['getdata']

    @task
    def set_single(self):
        mapping = utils.read_data(data_code=1)
        return self.stub.setSingle(
            Data(userID=mapping.get('userID')[0], name=mapping.get('name')[0], email=mapping.get('email')[0]))

    @task
    def set_multiples(self):
        mapping = utils.read_data(data_code=pow(10, random.randint(1, 3)))
        dict_data = Dict().data
        for u, n, e in zip(mapping.get('userID'), mapping.get('name'), mapping.get('email')):
            dict_data.append(Data(userID=u, name=n, email=e))

        self.stub.setMultiple(Dict(data=dict_data))

    def delete_keys(self, k_list: list = None):
        keys = KeyList().key_list

        for k in k_list:
            keys.append(Key(key=k))

        return self.stub.delKeys(KeyList(key_list=keys))
