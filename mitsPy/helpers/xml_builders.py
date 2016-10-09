from xml.etree.ElementTree import Element, SubElement, tostring


def dict_to_xml_subelement(xml_formatted_dict, element_for_inserting):
    if type(xml_formatted_dict) == type({}) and xml_formatted_dict != {}:

        keys_list = list(xml_formatted_dict.keys())

        for i in keys_list:

            if i[0] == '#':
                if type(element_for_inserting.text) == type(''):
                    element_for_inserting.text += xml_formatted_dict[i]
                else:
                    element_for_inserting.text = xml_formatted_dict[i]

            elif i[0] != '@' and i[0] != '':

                attrib_dict = {}
                if type(xml_formatted_dict[i]) == type({}):
                    keys_list_attrib = list(xml_formatted_dict[i].keys())

                    for k in keys_list_attrib:
                        if k[0] == '@':
                            attrib_dict[k[1:]] = xml_formatted_dict[i][k]

                if attrib_dict != {}:
                    sub_elem = SubElement(element_for_inserting, i, attrib=attrib_dict)
                else:
                    sub_elem = SubElement(element_for_inserting, i)

                if type(xml_formatted_dict[i]) == type({}) and xml_formatted_dict != {}:
                    dict_to_xml_subelement(xml_formatted_dict[i], sub_elem)

    else:
        raise UserWarning("xml_formatted_dict is not a dictionary",
                          xml_formatted_dict)


class XmlRequest:
    def __init__(self, request_type, prolog='<?xml version="1.0" encoding="UTF-8"?>'):

        self.xml_prolog = prolog

        if request_type == "get" or request_type == "set":
            self.request_type = request_type
        else:
            raise UserWarning("request type must be set to 'get' or 'set', it was set to " + request_type, request_type)

        self.xml_packet = Element("Packet")
        self.xml_command = SubElement(self.xml_packet, "Command")
        self.xml_command.text = request_type + "Request"
        self.xml_database_manager = SubElement(self.xml_packet, "DatabaseManager")

    def build_full(self):
        return self.xml_prolog + tostring(self.xml_packet).decode()


class XmlGetRequest:
    def __init__(self, database_manager_content={}):
        self.xml_base = XmlRequest(request_type="get")
        dict_to_xml_subelement(database_manager_content, self.xml_base.xml_database_manager)
        self.built = self.xml_base.build_full()

class XmlGetMnetRequest:
    def __init__(self, group_number, list_of_attributes):
        self.dict_of_attributes = {'@' + x:'"*"' for x in list_of_attributes}
        self.built = XmlGetRequest({"Mnet": self.dict_of_attributes})


class BuiltXml:
    def __init__(self):
        self.get_system_data = XmlGetRequest({"SystemData": {
            "@Version": "*",
            "@TempUnit": "*",
            "@Model": "*",
            "@FilterSign": "*",
            "@ShortName": "*",
            "@DateFormat": "*"
        }}).built

        self.get_area_list = XmlGetRequest({"ControlGroup": {"AreaList": ''}}).built
        self.get_area_group_list = XmlGetRequest({"ControlGroup": {"AreaGroupList": ''}}).built
        self.get_mnet_group_list = XmlGetRequest({"ControlGroup": {"MnetGroupList": ''}}).built
        self.get_mnet_list = XmlGetRequest({"ControlGroup": {"MnetList": ''}}).built
        self.get_ddc_info_list = XmlGetRequest({"ControlGroup": {"DdcInfoList": ''}}).built
        self.get_view_info_list = XmlGetRequest({"ControlGroup": {"ViewInfoList": ''}}).built
        self.get_mc_list = XmlGetRequest({"ControlGroup": {"McList": ''}}).built
        self.get_mc_name_list = XmlGetRequest({"ControlGroup": {"McNameList": ''}}).built
        self.get_function_list = XmlGetRequest({"FunctionControl": {"FunctionList": ''}}).built

    def get_mnet_bulk(self, group_number):
        return XmlGetMnetRequest(group_number=group_number, list_of_attributes=["Bulk"]).built
