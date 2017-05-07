from mitsPy.helpers.http_connector import ConnectionToController
from datetime import time
from mitsPy.mitsubishigroup import MitsubishiGroup
import asyncio


class MitsubishiController:
    def __init__(self, url, path="/servlet/MIMEReceiveServlet", loop=asyncio.get_event_loop()):
        self.group_info = None
        self.model = None
        self.version = None
        self.initialized = False
        self.last_refresh = None
        self.connection = ConnectionToController(url, path)
        self.commands = self.connection.sendCommand
        self.groups = []
        self.loop = loop

    @asyncio.coroutine
    def refresh(self, group_callback_fn=lambda x: None):

        self.group_info = (yield from self.commands.get_mnet_list())
        list_of_group_numbers = sorted(self.group_info)

        for i in list_of_group_numbers:
            self.groups.append(MitsubishiGroup(group_number=self.group_info[i]['number'],
                                               group_name=self.group_info[i]['name_web'],
                                               commands=self.commands, loop=self.loop))

        for i in self.groups:
            i.init_info()

        group_callback_fn(self.groups)

        self.initialized = True
        self.last_refresh = time()

    def initialize(self, group_callback_fn=lambda x: None):
        future = self.refresh(group_callback_fn)
        return self.loop.create_task(future)

