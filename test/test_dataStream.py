from unittest import TestCase
from mock import patch, Mock
from DataStream import DataStream
from Observer import Observer

END_MARKER = "#END"

TEST_DATA = "Hello World"


class ObserverTest(Observer):
    def __init__(self):
        self.dataStream = DataStream()
        #self.dataStream.register_observer(self)
        print "INIT"

    def update(self, obj=None):
        print obj


class TestDataStream(TestCase):
    pass

    def setUp(self):
        self.dataStream = DataStream()

    def testAppendData_NewIncompleteData_fullDataReceivedFalse(self):
        self.dataStream.append(TEST_DATA)
        self.assertFalse(self.dataStream.fullDataReceived)

    def testAppendData_NewCompleteData_fullDataReceivedTrue(self):
        self.dataStream.append(TEST_DATA + END_MARKER)
        self.assertTrue(self.dataStream.fullDataReceived)

    def testAppendData_NewFIRSTIncompleteTHENCompleteData_fullDataReceivedTrueANDEmptyStringData(self):
        self.dataStream.append(TEST_DATA)
        self.assertFalse(self.dataStream.fullDataReceived)
        second_data = "My name is alvaro"
        self.dataStream.append(second_data + END_MARKER)
        self.assertTrue(self.dataStream.fullDataReceived)
        self.assertEqual('', self.dataStream.data)

    def testAppendData_CompleteDataPlusExtraData_ExtraData(self):
        extra_data = "Extra Data!"
        self.dataStream.append(TEST_DATA + END_MARKER + extra_data)
        self.assertEqual(extra_data, self.dataStream.data)

    def testAppendData_SpecialCasesTEST_fullDataReceivedTrue(self):
        self.dataStream.append("Test")
        self.assertTrue(self.dataStream.fullDataReceived)

    def testAppendData_SpecialCasesCLIENTBAXTER_fullDataReceivedFalse(self):
        self.dataStream.append("CLIENTID#Baxter")
        self.assertFalse(self.dataStream.fullDataReceived)

    def test_ObjectWasNotified_Notified(self):
        observer = ObserverTest()
        mock = Mock(observer)
        self.dataStream.register_observer(mock)
        self.dataStream.append(TEST_DATA + END_MARKER)
        self.assertTrue(mock.update.called)

    def testUnregisterObserver_register_EmptyList(self):
        observer = ObserverTest()
        self.dataStream.register_observer(observer)
        self.assertIn(observer, self.dataStream.observers)
        self.dataStream.unregister_observer(observer)
        self.assertNotIn(observer, self.dataStream.observers)





