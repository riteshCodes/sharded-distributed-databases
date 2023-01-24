from concurrent import futures
import grpc

# import generated classes
from protos.comm_pb2 import *
from protos.comm_pb2_grpc import CommunicationServiceServicer, add_CommunicationServiceServicer_to_server

# import main (MWare class)
from main import MWare

m_ware = MWare()  # instance of middleware for calling operations

HOST = 'localhost'
PORT = '6379'


class Listener(CommunicationServiceServicer):
    """
    The listener function implements the rpc call as described in the .protos file
    """

    def testConnection(self, request, context):
        """
        The testConnection function takes a simple string message as request and returns a string message as response
         for testing the connection between middleware and client
        """
        return StringMessage(
            message=f'Request message from client: {request.message}, ' + 'Response message from middleware : OK')

    def getKeySpaceInfo(self, request, context):
        """

        """
        key_space_inf = MapStringInt().key_value  # response type

        for k, v in m_ware.key_space_inf().items():
            key_space_inf[k] = v

        return MapStringInt(key_value=key_space_inf)

    def getSingle(self, request, context):
        """

        """
        value = m_ware.get_all(hash_key_list=[request.key])
        print(value)
        if value:  # if the given key exists
            # Generate valid data
            print(value[0])
            return GetData(name=value[0].get('name'), email=value[0].get('email'))
        else:
            print("EMPTY")
            return GetData(name='EMPTY', email='EMPTY')  # if keys are not present [Test]

    def setSingle(self, request, context):
        """

        """
        m_ware.set_to(hash_key=request.userID, name=request.name, email=request.email)
        return StringMessage(message='OK')

    def getMultiple(self, request, context):
        """

        """
        keys = []
        for k in request.key_list:
            keys.append(k.key)
        values = m_ware.get_all(hash_key_list=keys)

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

        """
        uid_list = []
        name_list = []
        email_list = []
        for d in request.data:
            uid_list.append(d.userID)
            name_list.append(d.name)
            email_list.append(d.email)
        # TODO concurrent writes
        m_ware.set_multiples(key_list=uid_list, name_list=name_list, email_list=email_list)
        return StringMessage(message='OK')

    def delKeys(self, request, context):
        """

        """
        keys = []
        for k in request.key_list:
            keys.append(k.key)

        deleted = m_ware.del_keys(hash_key_list=keys)
        if deleted is None:
            return StringMessage(message='NONE')

        return StringMessage(message='OK')

    def getRange(self, request, context):
        """

        """
        res = GetDictData().getdata  # Valid response type
        values_list = m_ware.get_range(start=request.start, end=request.end)

        if values_list:
            for v in values_list:
                data = GetData(name=v.get('name'), email=v.get('email'))
                res.append(data)
        else:
            res.append(GetData(name='EMPTY', email='EMPTY'))

        return GetDictData(getdata=res)  # repeated getdata


def serve():
    """The main serve function of the server.
    This opens the socket, and listens for incoming grpc conformant packets"""

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CommunicationServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:6379")
    server.start()
    print('\nMiddleware is running ... \n')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('Middleware stopped.')


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
