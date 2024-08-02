# ScarxApi Python Client

Example Usage:

```
import asyncio
from scarx_api_client import ScarxApiChannel


async def main():
    with ScarxApiChannel("Test-Client", "ApiToken") as api:
        response = await api.IpServiceV1.get_ip(ip="1.1.1.1")
    print(response)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
```
