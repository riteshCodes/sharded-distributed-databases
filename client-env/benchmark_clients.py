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
        self.large_content = utils.read_data(data_code=1000)
        self.small_content = utils.read_data(data_code=10)

    # @task
    def ping(self):
        self.stub.testConnection(StringMessage(message='Ping Load Testing'))

    @task(1)
    def get_single(self):
        key_list = random.sample(self.small_content.get('userID'), 1)
        data = self.stub.getSingle(Key(key=key_list[0]))
        dict_data = MessageToDict(data)
        return dict_data

    @task(1)
    def get_multiples(self):
        keys = KeyList().key_list

        for k in self.large_content.get('userID'):
            keys.append(Key(key=k))

        proto_data = self.stub.getMultiple(KeyList(key_list=keys))

        dict_data = MessageToDict(proto_data)
        if isinstance(proto_data, GetDictData):
            return dict_data['getdata']

    @task(1)
    def get_range(self):
        start = random.randint(0, 999)
        end = start + 100  # range of 100 keys
        return MessageToDict(self.stub.getRange(Range(start=start, end=end)))['getdata']

    @task(1)
    def set_single(self):
        key = random.randint(0, 999)  # Random key-generation
        return self.stub.setSingle(
            Data(userID=key, name='set_single_test',
                 email='set_single_test'))

    @task(1)
    def set_multiples(self):
        dict_data = Dict().data
        for u, n, e in zip(self.large_content.get('userID'), self.large_content.get('name'),
                           self.large_content.get('email')):
            dict_data.append(Data(userID=u, name=n, email=e))

        self.stub.setMultiple(Dict(data=dict_data))

    @task(1)
    def del_single(self):
        key_list = random.sample(range(0, 999), 1)
        keys = KeyList().key_list

        keys.append(Key(key=key_list[0]))  # delete single key
        return self.stub.delKeys(KeyList(key_list=keys))

    @task(1)
    def del_multiples(self):
        key_list = random.sample(range(0, 999), 100)

        keys = KeyList().key_list

        for k in key_list:
            keys.append(Key(key=k))

        return self.stub.delKeys(KeyList(key_list=keys))

# locust -f benchmark_clients.py --csv=test_report_stats
