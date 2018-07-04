import aiohttp
import asyncio

from mitsPy.helpers.xml_builders import BuiltXml
from mitsPy.helpers.xml_parsers import Parsers

sem = asyncio.Semaphore(7)


async def post(session, url, data, headers):
  async with sem, session.post(url, data=data, headers=headers) as response:
    return await response.text()


class SendControllerCommands:
  def __init__(self, url, headers):
    self.url = url
    self.headers = headers

  async def post_to_controller(self, post_data):
    async with aiohttp.ClientSession() as session:
      return await post(session, self.url, data=post_data, headers=self.headers)

  async def get_system_data(self):
    return await self.post_to_controller(BuiltXml().get_system_data)

  async def get_area_list(self):
    return await self.post_to_controller(BuiltXml().get_area_list)

  async def get_area_group_list(self):
    return await self.post_to_controller(BuiltXml().get_area_group_list)

  async def get_mnet_group_list(self):
    return await self.post_to_controller(BuiltXml().get_mnet_group_list)

  async def get_mnet_list(self):
    response = await self.post_to_controller(BuiltXml().get_mnet_list)
    print(response)
    return Parsers().groups(data=response)

  async def get_ddc_info_list(self):
    return await self.post_to_controller(BuiltXml().get_ddc_info_list)

  async def get_view_info_list(self):
    return await self.post_to_controller(BuiltXml().get_view_info_list)

  async def get_mc_list(self):
    return await self.post_to_controller(BuiltXml().get_mc_list)

  async def get_mc_name_list(self):
    return await self.post_to_controller(BuiltXml().get_mc_name_list)

  async def get_function_list(self):
    return await self.post_to_controller(BuiltXml().get_function_list)

  async def get_mnet_bulk(self, group_number):
    response = (await self.post_to_controller(BuiltXml().get_mnet_bulk(group_number=group_number)))
    print(response)
    return (Parsers().bulk_from_single(response))

  async def get_basic_group_info(self, group_number):
    response = (await self.post_to_controller(BuiltXml().get_current_info(group_number=group_number)))
    return Parsers().all_basic_info(response, "SetbackControl")

  async def set_setback_control_items(self, group_number, item_dict):
    response = (await self.post_to_controller(
      BuiltXml().set_mnet_items(group_number=group_number, dict_of_items_to_set=item_dict)))
    return Parsers().all_basic_info(response,
                                    "SetbackControl")

  async def set_mnet_items(self, group_number, item_dict):
    response = (await self.post_to_controller(
      BuiltXml().set_mnet_items(group_number=group_number, dict_of_items_to_set=item_dict)))
    print(response)
    return Parsers().all_basic_info(response,
                                    "Mnet")

  async def get_current_drive(self, group_number):
    response = (await self.post_to_controller(BuiltXml().get_current_drive(group_number=group_number)))
    return Parsers().current_drive(response)


class ConnectionToController:
  def __init__(self, url, path="/servlet/MIMEReceiveServlet"):
    self.headers = {'Content-Type': 'text/xml'}
    self.url = url + path
    print("connecting to " + self.url)
    self.sendCommand = SendControllerCommands(self.url, self.headers)
