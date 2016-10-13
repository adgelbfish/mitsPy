import asyncio

from mitsPy.helpers.http_connector import ConnectionToController
from datetime import time
from mitsPy.mitsubishigroup import MitsubishiGroup


class MitsubishiController:
    def __init__(self, url, path="/servlet/MIMEReceiveServlet"):
        self.group_info = None
        self.model = None
        self.version = None
        self.initialized = False
        self.last_refresh = None
        self.connection = ConnectionToController(url, path)
        self.commands = self.connection.sendCommand
        self.groups = []

    def refresh(self):
        self.group_info = self.commands.get_mnet_list()
        list_of_group_numbers = sorted(self.group_info)

        try:
            loop = asyncio.get_event_loop()
            async def do_async():
                if self.group_info is not None and type(self.group_info) == dict:
                    for i in list_of_group_numbers:
                        await loop.run_in_executor(None, self.groups.append,
                                                   (MitsubishiGroup(group_number=self.group_info[i]['number'],
                                                                    group_name=self.group_info[i]['name_web'],
                                                                    commands=self.commands)))
                    for i in self.groups:
                        i.init_info()
                self.initialized = True
                self.last_refresh = time()

            loop = asyncio.get_event_loop()
            loop.run_until_complete(do_async())

        except:

            for i in list_of_group_numbers:
                self.groups.append(MitsubishiGroup(group_number=self.group_info[i]['number'],
                                                   group_name=self.group_info[i]['name_web'],
                                                   commands=self.commands))
            for i in self.groups:
                i.init_info()
            self.initialized = True
            self.last_refresh = time()


    def initialize(self):
        self.refresh()
