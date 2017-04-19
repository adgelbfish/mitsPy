from mitsPy.helpers.mnet_bulk_parser import MnetBulkParser
from mitsPy.helpers.temperature_utils import *
import asyncio


class MitsubishiGroup:
    def __init__(self, group_number, group_name, commands, loop = asyncio.get_event_loop()):
        self.number = group_number
        self.bulk = None
        self.commands = commands
        self.group_name = group_name
        self.current_temp_c = None
        self.current_temp_f = None
        self.basic_info = None
        self.air_direction_options = None
        self.current_air_direction = None
        self.current_drive = None
        self.current_mode = None
        self.current_operation = None
        self.operation_list = None
        self.mode_list = None
        self.set_temp_value_c = None
        self.set_temp_value_f = None
        self.fan_speed_options = None
        self.current_fan_speed = None
        self.loop = loop

    @asyncio.coroutine
    def _get_info(self):
        self.bulk = (yield from self.commands.get_mnet_bulk(group_number=self.number))
        self.set_temp_value_f = (MnetBulkParser(bulk_string=self.bulk).get_set_temp_f())
        self.current_temp_c = str((MnetBulkParser(bulk_string=self.bulk).get_current_temp_c()))
        self.current_temp_f = str(CelsiusToFahrenheit(self.current_temp_c).to_tenth)
        self.air_direction_options = (MnetBulkParser(bulk_string=self.bulk).get_air_direction_options())
        self.current_air_direction = (MnetBulkParser(bulk_string=self.bulk).get_current_air_direction())
        self.current_fan_speed = (MnetBulkParser(bulk_string=self.bulk).get_current_fan_speed())
        self.fan_speed_options = (MnetBulkParser(bulk_string=self.bulk).get_fan_speed_options())
        self.current_drive = (MnetBulkParser(bulk_string=self.bulk).get_current_drive())
        self.current_mode = (MnetBulkParser(bulk_string=self.bulk).get_current_mode())
        self.mode_list = ['FAN', 'COOL', 'HEAT', 'DRY']
        self.operation_list = ['FAN', 'COOL', 'HEAT', 'DRY', 'OFF']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive
        self.basic_info = (yield from self.commands.get_basic_group_info(group_number=self.number))

    def init_info(self):
        future = self._get_info()
        self.loop.create_task(future)

    def refresh(self):
        future = self._get_info()
        self.loop.create_task(future)

    def set_air_direction(self, direction):
        future = self._set_air_direction(direction=direction)
        self.loop.create_task(future)

    def set_drive(self, drive):
        future = self._set_drive(drive=drive)
        self.loop.create_task(future)

    def set_mode(self, mode):
        future = self._set_mode(mode=mode)
        self.loop.create_task(future)

    def set_mode_and_drive_on(self, mode):
        future = self._set_mode_and_drive_on(mode=mode)
        self.loop.create_task(future)

    def set_operation(self, operation):
        future = self._set_operation(operation=operation)
        self.loop.create_task(future)

    def set_temperature_f(self, desired_temp_string_f):
        future = self._set_temperature_f(desired_temp_string_f=desired_temp_string_f)
        self.loop.create_task(future)

    def set_fan_speed(self, desired_fan_speed):
        future = self._set_fan_speed(desired_fan_speed=desired_fan_speed)
        self.loop.create_task(future)

    @asyncio.coroutine
    def _set_air_direction(self, direction):
        response = (
            yield from self.commands.set_mnet_items(group_number=self.number, item_dict={'AirDirection': direction}))
        self.current_air_direction = response['AirDirection']

    @asyncio.coroutine
    def _set_drive(self, drive):
        response = (yield from self.commands.set_mnet_items(group_number=self.number, item_dict={'Drive': drive}))
        self.current_drive = response['Drive']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive

    @asyncio.coroutine
    def _set_mode(self, mode):
        response = (yield from self.commands.set_mnet_items(group_number=self.number, item_dict={'Mode': mode}))
        self.current_drive = response['Mode']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive

    @asyncio.coroutine
    def _set_mode_and_drive_on(self, mode):
        response = (
            yield from self.commands.set_mnet_items(group_number=self.number, item_dict={'Drive': 'ON', 'Mode': mode}))
        self.current_drive = response['Drive']
        self.current_mode = response['Mode']
        self.current_operation = self.current_mode if self.current_drive != 'OFF' else self.current_drive

    @asyncio.coroutine
    def _set_operation(self, operation):
        if operation == 'OFF':
            self._set_drive('OFF')
        else:
            self._set_mode_and_drive_on(operation)

    @asyncio.coroutine
    def _set_temperature_f(self, desired_temp_string_f):
        desired_temp_string_c = str(FahrenheitToCelsius(desired_temp_string_f).to_half_degree)
        response = (
            yield from self.commands.set_mnet_items(group_number=self.number,
                                                    item_dict={'SetTemp': desired_temp_string_c}))
        self.set_temp_value_c = response['SetTemp']

    @asyncio.coroutine
    def _set_fan_speed(self, desired_fan_speed):
        reponse = (
            yield from self.commands.set_mnet_items(group_number=self.number,
                                                    item_dict={'FanSpeed': desired_fan_speed}))
        self.current_fan_speed = reponse['FanSpeed']
