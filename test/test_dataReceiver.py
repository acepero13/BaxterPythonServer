from unittest import TestCase

from GenericDevice import GenericDevice
from src.customexceptions.CustomExceptions import MethodDoesNotExists, ExecutionException
from src.utils.datareceiver import DataReceiver

I_WAS_CALLED = "I was called"


class TestDevice(GenericDevice):
    def __init__(self):
        pass

    def test_method(self):
        return I_WAS_CALLED

    def test_method_with_params(self, params):
        print params
        return I_WAS_CALLED

    def test_method_raises_exception(self):
        raise Exception


class TestDataReceiver(TestCase):
    @staticmethod
    def make_receiver(data, test_device=None):
        if test_device is None:
            test_device = TestDevice()
        return DataReceiver(data, test_device)

    def test_PerformAction_None_None(self):
        data = None
        receiver = self.make_receiver(data)
        result = receiver.perform_action()
        self.assertIsNone(result)

    def test_PerformAction_ClientBaxter_None(self):  # Todo: Make return exception?
        data = "Client: Client#BaxterID"
        receiver = self.make_receiver(data)
        result = receiver.perform_action()
        self.assertIsNone(result)

    def test_PerformAction_ReservedAction_CloseConnectionStr(self):
        obj = dict()
        obj['method'] = "closeConnection"
        obj['params'] = ""
        receiver = self.make_receiver(obj)
        expected = "closeConnection"
        result = receiver.perform_action()
        self.assertEqual(expected, result)

    def test_PerformAction_TestActionNoParams_ExecuteFunctionCalled(self):
        obj = dict()
        obj['method'] = "test_method"
        obj['params'] = None
        test_device = TestDevice()
        receiver = self.make_receiver(obj, test_device)
        result = receiver.perform_action()
        self.assertEqual(I_WAS_CALLED, result)

    def test_PerformAction_TestActionWithParams_ExecuteFunctionCalled(self):
        obj = dict()
        obj['method'] = "test_method_with_params"
        obj['params'] = ["param1", "param2"]
        test_device = TestDevice()
        receiver = self.make_receiver(obj, test_device)
        result = receiver.perform_action()
        self.assertEqual(I_WAS_CALLED, result)

    def test_PerformAction_TestActionBadMethod_None(self):
        obj = dict()
        obj['metho'] = "test_method_with_params"
        test_device = TestDevice()
        receiver = self.make_receiver(obj, test_device)
        result = receiver.perform_action()
        self.assertEqual(None, result)

    def test_PerformAction_TestActionMethodDoesntExist_MethodDoesntExist(self):
        obj = dict()
        obj['method'] = "method_doesnt_exist"
        test_device = TestDevice()
        receiver = self.make_receiver(obj, test_device)
        self.assertRaises(MethodDoesNotExists, receiver.perform_action)

    def test_PerformAction_TestActionMethodRaiseException_RaiseMethod(self):
        obj = dict()
        obj['method'] = "test_method_raises_exception"
        test_device = TestDevice()
        receiver = self.make_receiver(obj, test_device)
        self.assertRaises(ExecutionException, receiver.perform_action)
