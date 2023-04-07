from concurrent import futures
import os
import grpc

# import generated classes
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceServicer, add_CommunicationServiceServicer_to_server

# import main (MWare class)
from main import MWare

# m_ware = MWare()  # instance of middleware for calling operations

HOST = 'localhost'
PORT = '6379'


class Listener(CommunicationServiceServicer):
    """
    The listener class functions implement the rpc calls as described in the .protos file
    """

    def __init__(self):
        self.m_ware = MWare()

    def testConnection(self, request, context):
        """
        testConnection function takes a simple string message as request and returns a string message as response
         for testing the connection between middleware and client
        """
        return StringMessage(
            message=f'Request message from client: {request.message}, ' + 'Response message from middleware : OK')

    def getKeySpaceInfo(self, request, context):
        """
        getKeySpaceInfo returns a string-int key-value pairs with database url as string and number of keys stored in
        corresponding database as int
        """
        key_space_inf = MapStringInt().key_value  # response type

        for k, v in self.m_ware.key_space_inf().items():
            key_space_inf[k] = v

        return MapStringInt(key_value=key_space_inf)

    def getSingle(self, request, context):
        """
        getSingle returns associated value of given key (single key) if it exits in database, else returns an empty
        value
        """
        value = self.m_ware.get_all(key_list=[request.key])
        if value:  # if the given key exists
            # Generate valid data
            return GetData(name=value[0].get('name'), email=value[0].get('email'))
        else:
            return GetData(name='EMPTY', email='EMPTY')  # if keys are not present [Test]

    def setSingle(self, request, context):
        """
        setSingle stores a single key-value pair in corresponding database
        """
        self.m_ware.set_to(key=request.userID, name=request.name, email=request.email)
        return StringMessage(message='OK')

    def getMultiple(self, request, context):
        """
        getMultiple returns associated values of given keys (multiple keys) if they exits in database, else returns an
        empty value for the key, which is not present
        """
        keys = []
        for k in request.key_list:
            keys.append(k.key)
        values = self.m_ware.get_all(key_list=keys)

        response = GetDictData().getdata

        if values:  # values for given keys exit
            for i in values:
                single_data = GetData(name=i.get('name'), email=i.get('email'))
                response.append(single_data)
        else:
            response.append(GetData(name='EMPTY', email='EMPTY'))  # if keys are not present [Test]

        return GetDictData(getdata=response)  # repeated getdata

    def setMultiple(self, request, context):
        """
        setMultiple stores multiple key-value pairs in corresponding database atomically
        """
        uid_list = []
        name_list = []
        email_list = []
        for d in request.data:
            uid_list.append(d.userID)
            name_list.append(d.name)
            email_list.append(d.email)
        self.m_ware.set_multiples(key_list=uid_list, name_list=name_list, email_list=email_list)
        return StringMessage(message='OK')

    def delKeys(self, request, context):
        """
        delKeys deletes single/multiple key-value pairs from corresponding database atomically
        """
        keys = []
        for k in request.key_list:
            keys.append(k.key)

        deleted = self.m_ware.del_keys(key_list=keys)
        if deleted is None:
            return StringMessage(message='NONE')

        return StringMessage(message='OK')

    def getRange(self, request, context):
        """
        getRange returns associated values of given key range (inclusive range) if they exits in database, else returns
        an empty value for the key, which is not present
        """
        res = GetDictData().getdata  # Valid response type
        values_list = self.m_ware.get_range(start=request.start, end=request.end)

        if values_list:
            for v in values_list:
                data = GetData(name=v.get('name'), email=v.get('email'))
                res.append(data)
        else:
            res.append(GetData(name='EMPTY', email='EMPTY'))

        return GetDictData(getdata=res)  # repeated getdata


def serve():
    """
    The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=os.cpu_count()))
    add_CommunicationServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:6379")
    server.start()
    print_msg_box('\n ... MIDDLEWARE IS RUNNING ... \n')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\n ... \n')
        print_msg_box('MIDDLEWARE STOPPED')


def print_msg_box(msg, indent=1, width=None, title=None):
    """Print start up message"""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)


def parse_to_data(dict_data):
    res = []
    for d in dict_data:
        data = Data()
        data.userID = d.get('userID')
        data.name = d.get('name')
        data.email = d.get('email')
        res.append(data)
    return res


if __name__ == "__main__":
    serve()
