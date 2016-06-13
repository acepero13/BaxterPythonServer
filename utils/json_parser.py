import json


class JsonParser(object):
    def __init__(self):
        pass

    def parse(self, string):
        try:
            json_object = json.loads(string)
            return json_object
        except:
            return False

    def writeJson(self, data):
        try:
            result = json.dumps(data)
            return result
        except:
            print "Problem writing json"
            return False