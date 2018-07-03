
import asyncio
from concurrent.futures import ThreadPoolExecutor

from mitsPy import manager
loop2 = asyncio.new_event_loop()
loop = asyncio.new_event_loop()
loop2.run_in_executor(ThreadPoolExecutor(max_workers=1), lambda x: x.run_forever(), loop)
hvac = manager.Manager("http://domain.tld", loop=loop)

hvac.initialize()

groups = hvac.groups

for group in groups:
    group.init_info(lambda x: print("done"))
    print(group)


