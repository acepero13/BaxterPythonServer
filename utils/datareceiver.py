import test
from utils.parsers import Parser


class DataReceiver(object):
    def __init__(self):
        self.parser = Parser()

    def perform(self, data):
        response = list()
        return 1
        obj = self.parser.parse(data)
        if not obj and isinstance(data, str):
            if "#" in data:
                self.client = data[data.find("#")+1:]
                print "CLIENT: " + self.client
            return None
        method = obj['method']
        params = obj['params']
        if method == 'closeConnection':
            return 'closeConnection'
        gestures = test.DummyClass()
        methods = [method_iter for method_iter in dir(gestures) if callable(getattr(gestures, method_iter))]
        if method in methods:
            try:
                func = getattr(gestures, method)
                if len(params) > 0 and params != None and params != "null":
                    res = func(params)
                else:
                    res = func()
            except AttributeError:
                print "dostuff not found"
        print res
        return res
