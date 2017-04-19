import asyncio

import aiohttp

from mitsPy.helpers.xml_builders import BuiltXml
from mitsPy.helpers.xml_parsers import Parsers

sem = asyncio.Semaphore(7)


@asyncio.coroutine
def post(session, url, data, headers):
    with (yield from sem):
        response = yield from session.post(url, data=data, headers=headers)
        return (yield from response.text())


class SendControllerCommands:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    @asyncio.coroutine
    def post_to_controller(self, post_data):
        print(post_data)
        with aiohttp.ClientSession() as session:
            return (yield from post(session, self.url, data=post_data, headers=self.headers))

    @asyncio.coroutine
    def get_system_data(self):
        return (yield from self.post_to_controller(BuiltXml().get_system_data))

    @asyncio.coroutine
    def get_area_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_area_list))

    @asyncio.coroutine
    def get_area_group_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_area_group_list))

    @asyncio.coroutine
    def get_mnet_group_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_mnet_group_list))

    @asyncio.coroutine
    def get_mnet_list(self):
        response = (yield from self.post_to_controller(BuiltXml().get_mnet_list))
        return Parsers().groups(data=response)

    @asyncio.coroutine
    def get_ddc_info_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_ddc_info_list))

    @asyncio.coroutine
    def get_view_info_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_view_info_list))

    @asyncio.coroutine
    def get_mc_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_mc_list))

    @asyncio.coroutine
    def get_mc_name_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_mc_name_list))

    @asyncio.coroutine
    def get_function_list(self):
        return (yield from self.post_to_controller(BuiltXml().get_function_list))

    @asyncio.coroutine
    def get_mnet_bulk(self, group_number):
        response = (yield from self.post_to_controller(BuiltXml().get_mnet_bulk(group_number=group_number)))
        return (Parsers().bulk_from_single(response))

    @asyncio.coroutine
    def get_basic_group_info(self, group_number):
        response = (yield from self.post_to_controller(BuiltXml().get_current_info(group_number=group_number)))
        return Parsers().all_basic_info(response, "SetbackControl")

    @asyncio.coroutine
    def set_setback_control_items(self, group_number, item_dict):
        response = (yield from self.post_to_controller(
            BuiltXml().set_mnet_items(group_number=group_number, dict_of_items_to_set=item_dict)))
        return Parsers().all_basic_info(response,
                                        "SetbackControl")

    @asyncio.coroutine
    def set_mnet_items(self, group_number, item_dict):
        response = (yield from self.post_to_controller(
            BuiltXml().set_mnet_items(group_number=group_number, dict_of_items_to_set=item_dict)))
        return Parsers().all_basic_info(response,
                                        "Mnet")

    @asyncio.coroutine
    def get_current_drive(self, group_number):
        response = (yield from self.post_to_controller(BuiltXml().get_current_drive(group_number=group_number)))
        return Parsers().current_drive(response)


class ConnectionToController:
    def __init__(self, url, path="/servlet/MIMEReceiveServlet"):
        self.headers = {'Content-Type': 'text/xml'}
        self.url = url + path
        self.sendCommand = SendControllerCommands(self.url, self.headers)
