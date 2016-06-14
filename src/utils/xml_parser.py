import xml.etree.ElementTree as ET


class XMLParser(object):
    def __init__(self):
        pass

    def parse(self, string):
        root = self.read_xml(string)
        obj = dict()
        if root.tag == 'Command':
            self.parse_command(obj, root)
        else:
            raise Exception('Command not specified')
        return obj

    @staticmethod
    def read_xml(string):
        try:
            root = ET.fromstring(string)
        except:
            raise Exception('A problem has occurred parsing xml')
        return root

    def parse_command(self, obj, root):
        if root.attrib:
            self.build_command_object(obj, root)
        else:
            raise Exception('Method not defined')

    @staticmethod
    def build_command_object(obj, root):
        obj['method'] = root.attrib['method']
        params_list = list()
        for param in root.iter('param'):
            params_list.append(param.text)
        obj['params'] = params_list

