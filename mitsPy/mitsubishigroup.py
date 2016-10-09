# class mitsubishi_group:
#     def __init__(self,
#                  group,
#                  fan_speed,
#                  direction,
#                  type=None):
#         self.fan_speed = fan_speed
#         self.direction = direction
#         self.type = type
#         self.group = group
#
#     def set_fan_speed(self, new_speed):
#         self.fan_speed = new_speed
from mitsPy.helpers.mnet_bulk_parser import MnetBulkParser


class MitsubishiGroup:
    def __init__(self, group_number, group_name, commands):
        self.number = group_number
        self.bulk = None
        self.commands= commands
        self.group_name = group_name
        self.current_temp_c = None

    def get_bulk(self):
        self.bulk = self.commands.get_mnet_bulk(group_number=self.number)
        self.current_temp_c = MnetBulkParser(bulk_string= self.bulk).get_current_temp_c()

    def init_info(self):
        self.get_bulk()
