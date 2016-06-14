from src.customexceptions.CustomExceptions import MethodDoesNotExists, ExecutionException
from src.utils.parsers import Parser


# TODO: Add logger

class DataReceiver(object):
    def __init__(self, obj, dev):
        self.parser = Parser()
        self.method = None
        self.params = list()
        self.data = obj
        self.device = dev
        self.gestures = list()
        if self.is_proper_object():
            self.method = self.data['method']
            self.add_params()
        self.reserved_actions = ["closeConnection"]

    def perform_action(self):
        if isinstance(self.data, str):
            return None
        if self.method is not None and self.is_reserved_action():
            return self.method
        if self.method:
            return self.execute_device_method()

    def is_proper_object(self):
        if isinstance(self.data, dict) and 'method' in self.data:
            return True
        return False

    def is_reserved_action(self):
        if self.method in self.reserved_actions:
            return True
        return False

    def execute_device_method(self):
        callable_methods = self.get_callable_methdos_from_obj()
        if self.method in callable_methods:
            try:
                return self.execute_method()
            except Exception, err:
                print err
                raise ExecutionException
        else:
            raise MethodDoesNotExists

    def get_callable_methdos_from_obj(self):
        return [method_iter for method_iter in dir(self.device) if callable(getattr(self.device, method_iter))]

    def execute_method(self):
        func = getattr(self.device, self.method)
        if self.params is not None and len(self.params) > 0 and self.params != "null":
            result_from_call = func(self.params)
        else:
            result_from_call = func()
        return result_from_call

    def add_params(self):
        if 'params' in self.data:
            self.params = self.data['params']
