'''
    CurrentDrive = 3
    CurrentMode = 5
    CurrentTemp_1 = 7
    CurrentTemp_2 = 9
    Temp_1 = 12
    Temp_2 = 13
    CurrentDirection = 15
    CurrentFanSpeed = 17
    DriveItem = 21
    ModeItem = 23
    TempItem = 25
    FilterItem = 27
    AD_No_Feature = 53
    AD_4_Feature = 55
    FanSpeedSetting = 95
'''


class MnetBulkParser:
    def __init__(self, bulk_string):
        self.bulk_string = bulk_string

    def get_current_temp_c(self):
        return int('0x' + self.bulk_string[12] + self.bulk_string[13], 16) / 10

    def get_air_direction_options(self):
        if self.bulk_string[53] == '0':
            air_direction_options = None
        elif self.bulk_string[55] == '0':
            air_direction_options = ['VERTICAL', 'MID2', 'MID1', 'HORIZONTAL']
        else:
            air_direction_options = ['VERTICAL', 'MID2', 'MID1', 'MID0', 'HORIZONTAL',
                                     'SWING', 'AUTO']
        return air_direction_options

    def get_current_air_direction(self):
        return ['SWING', 'VERTICAL', 'MID2', 'MID1', 'HORIZONTAL', 'MID0', 'AUTO'][int(self.bulk_string[15])]

    def get_current_drive(self):
        return ['OFF', 'ON'][int(self.bulk_string[3])]

    def get_current_mode(self):
        return ['FAN', 'COOL', 'HEAT', 'DRY'][int(self.bulk_string[5])]

    def get_set_temp(self):
        val1 = int(self.bulk_string[7], 16)
        val2 = int(self.bulk_string[9])
        v = val1 * 10 + val2 - 10
        if val1 == 4:
            v -= 5
        if val1 >= 5:
            v -= 10
        return str(v / 5 + 63)
