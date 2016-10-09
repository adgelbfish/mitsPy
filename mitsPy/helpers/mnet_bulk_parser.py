
class MnetBulkParser:
    def __init__(self, bulk_string):
        self.bulk_string = bulk_string

    def get_current_temp_c(self):
        print(int('0x' + self.bulk_string[12] + self.bulk_string[13], 16)/10)
        return int('0x' + self.bulk_string[12] + self.bulk_string[13], 16)/10
