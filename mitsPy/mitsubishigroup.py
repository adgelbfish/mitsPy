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
        self.mode_list = None
        self.set_temp = None

    def get_info(self):
        self.bulk = self.commands.get_mnet_bulk(group_number=self.number)
        self.set_temp = MnetBulkParser(bulk_string=self.bulk).get_set_temp()
        self.current_temp_c = str(MnetBulkParser(bulk_string=self.bulk).get_current_temp_c())
        self.air_direction_options = MnetBulkParser(bulk_string=self.bulk).get_air_direction_options()
        self.current_air_direction = MnetBulkParser(bulk_string=self.bulk).get_current_air_direction()
        self.current_drive = MnetBulkParser(bulk_string=self.bulk).get_current_drive()
        self.current_mode = MnetBulkParser(bulk_string=self.bulk).get_current_mode()
        self.mode_list = ['FAN', 'COOL', 'HEAT', 'DRY']
        self.operation_list = ['FAN', 'COOL', 'HEAT', 'DRY', 'OFF']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive
        self.basic_info = self.commands.get_basic_group_info(group_number=self.number)

    def init_info(self):
        self.get_info()

    def refresh(self):
        self.get_info()

    def set_air_direction(self, direction):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'AirDirection': direction})
        self.current_air_direction = response['AirDirection']

    def set_drive(self, drive):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'Drive': drive})
        self.current_drive = response['Drive']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive

    def set_mode(self, mode):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'Mode': mode})
        self.current_drive = response['Mode']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive

    def set_mode_and_drive_on(self, mode):
        response = self.commands.set_mnet_items(group_number=self.number, item_dict={'Drive': 'ON', 'Mode': mode})
        self.current_drive = response['Drive']
        self.current_mode = response['Mode']
        print(self.current_mode)
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive
        print(self.current_operation)

    def set_operation(self, operation):
        if operation == 'OFF':
            self.set_drive('OFF')
        else:
            self.set_mode_and_drive_on(operation)


