from Observable import Observable
from src.utils.parsers import Parser

END_MARKER = "#END"

TEST = "Test"  # Only for testing purposes

CLIENTID_BAXTER = 'CLIENTID#Baxter'


class DataStream(Observable):
    def __init__(self):
        self.observers = list()
        self.data = ""
        self.fullDataReceived = False
        self.parser = Parser()

    def notify_all(self, obj=None):
        for observer in self.observers:
            observer.update(obj)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def register_observer(self, observer):
        self.observers.append(observer)

    def append(self, data_received):
        data_received = data_received.strip()
        if data_received == TEST:
            self.mark_fulldata_as_received()
            self.notify_all()
        elif data_received == CLIENTID_BAXTER:
            self.client_baxter_was_received()
        elif END_MARKER not in data_received:
            self.append_not_full_data(data_received)
        else:
            self.full_data_was_received_and_notify(data_received)
            self.mark_fulldata_as_received()

    def mark_fulldata_as_received(self):
        self.fullDataReceived = True

    def full_data_was_received_and_notify(self, data_received):
        pos = data_received.index(END_MARKER)
        self.data += data_received[:pos]
        obj = self.parser.parse(self.data)
        self.data = data_received[pos + len(END_MARKER):]
        self.notify_all(obj)

    def append_not_full_data(self, data_received):
        self.data += data_received

    @staticmethod
    def client_baxter_was_received():
        print "Initial data received, nothing to be done"

