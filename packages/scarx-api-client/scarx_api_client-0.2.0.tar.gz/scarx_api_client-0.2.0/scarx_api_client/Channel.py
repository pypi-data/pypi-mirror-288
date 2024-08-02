from grpclib.client import Channel
from scarx_api_client.proto.grpc.api.v1 import IpServiceStub, LakGatewayServiceStub, LakConfigurationServiceStub, LakDataServiceStub


class ScarxApiChannel:
    def __init__(self, client_name: str, api_token: str):
        self.__channel = Channel(host="api.scarx.net", port=443, ssl=True)
        self.IpServiceV1 = IpServiceStub(self.__channel, metadata={
            "client-name": client_name,
            "api-token": api_token
        })
        self.LakGatewayServiceV1 = LakGatewayServiceStub(self.__channel, metadata={
            "client-name": client_name,
            "api-token": api_token
        })
        self.LakConfigurationServiceV1 = LakConfigurationServiceStub(self.__channel, metadata={
            "client-name": client_name,
            "api-token": api_token
        })
        self.LakDataServiceV1 = LakDataServiceStub(self.__channel, metadata={
            "client-name": client_name,
            "api-token": api_token
        })

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__channel.close()
