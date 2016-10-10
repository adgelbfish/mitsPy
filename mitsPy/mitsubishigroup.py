from mitsPy.helpers.mnet_bulk_parser import MnetBulkParser


class MitsubishiGroup:
    def __init__(self, group_number, group_name, commands):
        self.number = group_number
        self.bulk = None
        self.commands = commands
        self.group_name = group_name
        self.current_temp_c = None
        self.basic_info = None
        self.air_direction_options = None
        self.current_air_direction = None
        self._http_lock = False
        print(group_number)

    def get_info(self):

        self.bulk = self.commands.get_mnet_bulk(group_number=self.number)
        self.current_temp_c = str(MnetBulkParser(bulk_string=self.bulk).get_current_temp_c())
        self.air_direction_options = MnetBulkParser(bulk_string=self.bulk).get_air_direction_options()
        self.current_air_direction = MnetBulkParser(bulk_string=self.bulk).get_current_air_direction()
        self.basic_info = self.commands.get_basic_group_info(group_number=self.number)

    def init_info(self):
            self.get_info()

    def refresh(self):
            self.get_info()

    def set_air_direction(self, direction):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'AirDirection': direction})
        self.current_air_direction = response['AirDirection']
