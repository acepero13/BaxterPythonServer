from src.utils.xml_parser import XMLParser


class CommandParser(object):
    def __init__(self):
        self.text = ""
        self.id = ""
        self.type = ""

    def parse(self, xml):
        root = XMLParser.read_xml(xml)
        message = root.find("message")
        if message is not None:
            self.text = message.text
            self.id = message.attrib['id']
            self.type = message.attrib['type']

    def getMessage(self):
        return self.text