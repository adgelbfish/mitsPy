from requests import post
from mitsPy.helpers.xml_builders import BuiltXml
from mitsPy.helpers.xml_parsers import Parsers

class SendControllerCommands:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def post_to_controller(self, post_data):
        return post(self.url, data=post_data, headers=self.headers).content.decode()

    def get_system_data(self):
        return self.post_to_controller(BuiltXml().get_system_data)

    def get_area_list(self):
        return self.post_to_controller(BuiltXml().get_area_list)

    def get_area_group_list(self):
        return self.post_to_controller(BuiltXml().get_area_group_list)

    def get_mnet_group_list(self):
        return self.post_to_controller(BuiltXml().get_mnet_group_list)

    def get_mnet_list(self):
        return Parsers.groups(data=self.post_to_controller(BuiltXml().get_mnet_list))

    def get_ddc_info_list(self):
        return self.post_to_controller(BuiltXml().get_ddc_info_list)

    def get_view_info_list(self):
        return self.post_to_controller(BuiltXml().get_view_info_list)

    def get_mc_list(self):
        return self.post_to_controller(BuiltXml().get_mc_list)

    def get_mc_name_list(self):
        return self.post_to_controller(BuiltXml().get_mc_name_list)

    def get_function_list(self):
        return self.post_to_controller(BuiltXml().get_function_list)

    def get_mnet_bulk(self, group_number):
        return self.post_to_controller(BuiltXml().get_mnet_bulk(group_number=group_number))



class ConnectionToController:
    def __init__(self, url, path="/servlet/MIMEReceiveServlet"):
        self.headers = {'Content-Type': 'text/xml'}
        self.url = url + path
        self.sendCommand = SendControllerCommands(self.url, self.headers)
