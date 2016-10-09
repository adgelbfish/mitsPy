from xmltodict import parse


class Parsers:
    def groups(data):
        group_dict = {}
        for i in parse(data)['Packet']['DatabaseManager']['ControlGroup']['MnetList']['MnetRecord']:
            group_dict[i['@Group']] = {
                'number': i['@Group'],
                'name_web': i['@GroupNameWeb'],
                'name_lcd': i['@GroupNameLcd']
            }
        return group_dict
