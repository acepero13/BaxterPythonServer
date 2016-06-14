import test
from utils.parsers import Parser


class DataReceiver(object):
    def __init__(self, obj):
        self.parser = Parser()
        self.method = None
        self.params = None
        self.data = obj
        self.gestures = list()
        if self.is_proper_object():
            self.method = self.data['method']
            self.params = self.data['params']
        self.reserved_actions = ["closeConnection"]

    def perform_action(self):
        if isinstance(self.data, str):
            return None
        if self.method is not None and self.is_reserved_action():
            return self.method

    def is_proper_object(self):
        if isinstance(self.data, dict) and self.data['method'] is not None:
            return True
        return False

    def is_reserved_action(self):
        if self.method in self.reserved_actions:
            return True
        return False



