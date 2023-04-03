import random

from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceStub
from locust import task

from google.protobuf.json_format import MessageToDict

import base_client
import utils


class BenchmarkingClient(base_client.BaseUser):
    host = '10.0.2.87:6379'  # middleware address
    stub_class = CommunicationServiceStub

    def __init__(self, environment):
        super().__init__(environment)
        self.mapping = utils.read_data(data_code=random.choice([1, 10, 100, 1000]))
        # self.single_mapping = utils.read_data(data_code=1)
        # self.multiple_mapping = utils.read_data(data_code=random.choice([10, 100, 1000]))
        self.single_mapping = utils.read_data(data_code=1)
        self.multiple_mapping = utils.read_data(data_code=random.choice([10, 100, 1000]))

    # @task
    def ping(self):
        self.stub.testConnection(StringMessage(message='Ping Load Testing'))

    @task
    def get_single(self):
        data = self.stub.getSingle(Key(key=self.single_mapping.get('userID')[0]))
        dict_data = MessageToDict(data)
        return dict_data

    @task
    def get_multiples(self):
        keys = KeyList().key_list

        for k in self.multiple_mapping.get('userID'):
            keys.append(Key(key=k))

        proto_data = self.stub.getMultiple(KeyList(key_list=keys))

        dict_data = MessageToDict(proto_data)
        if isinstance(proto_data, GetDictData):
            return dict_data['getdata']

    @task
    def get_range(self):
        start = 0
        end = random.choice([0, 9, 99, 999])  # anywhere between 1, 10, 100, 1000 key-value pairs
        return MessageToDict(self.stub.getRange(Range(start=start, end=end)))['getdata']

    @task
    def set_single(self):
        return self.stub.setSingle(
            Data(userID=self.single_mapping.get('userID')[0], name=self.single_mapping.get('name')[0],
                 email=self.single_mapping.get('email')[0]))

    @task
    def set_multiples(self):
        dict_data = Dict().data
        for u, n, e in zip(self.multiple_mapping.get('userID'), self.multiple_mapping.get('name'),
                           self.multiple_mapping.get('email')):
            dict_data.append(Data(userID=u, name=n, email=e))

        self.stub.setMultiple(Dict(data=dict_data))

    @task
    def delete_keys(self):
        k_list = self.mapping.get('userID')
        keys = KeyList().key_list

        for k in k_list:
            keys.append(Key(key=k))

        return self.stub.delKeys(KeyList(key_list=keys))
