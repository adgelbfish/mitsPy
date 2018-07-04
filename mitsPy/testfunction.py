
import asyncio
from concurrent.futures import ThreadPoolExecutor

from mitsPy import manager
loop2 = asyncio.new_event_loop()
loop = asyncio.new_event_loop()
hvac = manager.Manager("http://domain.tld")
async def start():
    await hvac.initialize()

    groups = hvac.groups

    for group in groups:
        await group.init_info(lambda: print("done"))
        print(group)

loop.run_until_complete(start())


