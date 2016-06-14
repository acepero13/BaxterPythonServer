from src.utils.json_parser import JsonParser
from src.utils.xml_parser import XMLParser


class Parser(object):
    def __init__(self):
        self.xml_par = XMLParser()
        self.json_par = JsonParser()

    def parse(self, data):
        if isinstance(data, str):
            if data[0] == '<':  # Probably is an xml
                try:
                    return self.xml_par.parse(data)
                except Exception as e:  # Let's try with json
                    if e.message == 'A problem has occurred parsing xml':
                        return self.json_par.parse(data)
            else:
                return self.json_par.parse(data)



