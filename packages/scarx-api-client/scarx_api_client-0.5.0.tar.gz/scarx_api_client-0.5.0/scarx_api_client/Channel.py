from typing import Mapping, Union, Callable, AsyncGenerator, Coroutine

from grpclib.client import Channel
from scarx_api_client.proto.grpc.api.v1 import IpServiceStub, LakGatewayServiceStub, LakConfigurationServiceStub, \
    LakDataServiceStub, LakInteractiveServiceStub, IpDetails, LakIosDeviceConfiguration, LakAndroidDeviceConfiguration, \
    LakGatewayStatus, LakCreateAccountStatus, LakAllianceHelpInfoStatus


class InternalScarxApiChannel:
    def __init__(self, channel: Channel, metadata: Mapping[str, Union[str, bytes]]):
        self.IpServiceV1 = IpServiceStub(channel, metadata=metadata)
        self.LakGatewayServiceV1 = LakGatewayServiceStub(channel, metadata=metadata)
        self.LakConfigurationServiceV1 = LakConfigurationServiceStub(channel, metadata=metadata)
        self.LakDataServiceV1 = LakDataServiceStub(channel, metadata=metadata)
        self.LakInteractiveServiceV1 = LakInteractiveServiceStub(channel, metadata=metadata)


class ScarxApiV1Lak:
    def __init__(self, api: InternalScarxApiChannel):
        self.Gateway = api.LakGatewayServiceV1
        self.Configuration = api.LakConfigurationServiceV1
        self.Data = api.LakDataServiceV1
        self.Interactive = api.LakInteractiveServiceV1


class ScarxApiChannelV1:
    def __init__(self, api: InternalScarxApiChannel):
        self.Ip = api.IpServiceV1
        self.Lak = ScarxApiV1Lak(api)


class ScarxApiChannel:
    def __init__(self, client_name: str, api_token: str):
        self.__channel = Channel(host="api.scarx.net", port=443, ssl=True)
        api = InternalScarxApiChannel(self.__channel, {
            "client-name": client_name,
            "api-token": api_token
        })
        self.Helper = ScarxApiHelper(self)
        self.V1 = ScarxApiChannelV1(api)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__channel.close()


class ScarxApiHelper:
    def __init__(self, api: ScarxApiChannel):
        self.__api = api

    async def easy_process_v1_lak_gateway(self,
                                          request_func: Callable[[LakGatewayServiceStub], AsyncGenerator[LakGatewayStatus, None]],
                                          status_func: Callable[[LakGatewayStatus], Coroutine] = None) -> LakGatewayStatus:
        final = None
        async for x in request_func(self.__api.V1.Lak.Gateway):
            if x.is_finished:
                final = x
            else:
                await status_func(x)
        if final is None:
            raise Exception("Process finished without Result!")
        return final

    async def easy_process_v1_lak_interactive_create_account(self,
                                                             world_id: int,
                                                             email: str,
                                                             password: str,
                                                             ip_id: str,
                                                             nickname: str,
                                                             *,
                                                             status_func: Callable[[LakCreateAccountStatus], Coroutine] = None) -> LakCreateAccountStatus:
        final = None
        async for x in self.__api.V1.Lak.Interactive.process_lak_create_account(world_id=world_id, email=email, password=password, ip_id=ip_id, nickname=nickname):
            if x.is_finished:
                final = x
            else:
                if status_func:
                    await status_func(x)
        if final is None:
            raise Exception("Process finished without Result!")
        return final

    async def easy_process_v1_lak_interactive_get_alliance_help(self,
                                                                world_id: int,
                                                                email: str,
                                                                password: str,
                                                                ip_id: str,
                                                                *,
                                                                status_func: Callable[[LakAllianceHelpInfoStatus], Coroutine] = None) -> LakAllianceHelpInfoStatus:
        final = None
        async for x in self.__api.V1.Lak.Interactive.process_get_alliance_help_info(world_id=world_id, email=email, password=password, ip_id=ip_id):
            if x.is_finished:
                final = x
            else:
                if status_func:
                    await status_func(x)
        if final is None:
            raise Exception("Process finished without Result!")
        return final
