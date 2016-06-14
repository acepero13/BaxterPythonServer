from unittest import TestCase

from utils.datareceiver import DataReceiver


class TestDataReceiver(TestCase):

    def make_receiver(self, data):
        return DataReceiver(data)

    def test_PerformAction_None_None(self):
        data = None
        receiver = self.make_receiver(data)
        result = receiver.perform_action()
        self.assertIsNone(result)

    def test_PerformAction_ClientBaxter_None(self): #Todo: Make return exception?
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

    def test_PerformAction_PaintAction_ExecuteFunctionCalled(self):
        obj = dict()
        obj['method'] = "paint"
        obj['params'] = "test"
        receiver = self.make_receiver(obj)
        #mock = Mock(receiver.par)
        #result = receiver.perform_action()
        #self.assertEqual(expected, result)

