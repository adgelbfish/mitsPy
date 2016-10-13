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
        self.current_drive = None
        self.current_mode = None
        self.current_operation = None
        self.operation_list = None

    def get_info(self):

        self.bulk = self.commands.get_mnet_bulk(group_number=self.number)
        self.current_temp_c = str(MnetBulkParser(bulk_string=self.bulk).get_current_temp_c())
        self.air_direction_options = MnetBulkParser(bulk_string=self.bulk).get_air_direction_options()
        self.current_air_direction = MnetBulkParser(bulk_string=self.bulk).get_current_air_direction()
        self.current_drive = self.commands.get_current_drive(self.number)
        self.current_mode = MnetBulkParser(bulk_string=self.bulk).get_current_mode()
        self.mode_list = ['FAN', 'COOL', 'HEAT', 'DRY']
        self.operation_list = ['FAN', 'COOL', 'HEAT', 'DRY', 'CHK_OFF']
        self.current_operation = self.current_mode if self.current_drive != 'CHK_OFF' else self.current_drive
        self.basic_info = self.commands.get_basic_group_info(group_number=self.number)


    def init_info(self):
        self.get_info()

    def refresh(self):
        self.get_info()

    def set_air_direction(self, direction):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'AirDirection': direction})
        self.current_air_direction = response['AirDirection']

