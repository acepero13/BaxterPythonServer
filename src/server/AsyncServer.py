from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, Protocol

from DataStream import DataStream
from Observer import Observer
from src.utils.datareceiver import DataReceiver

SERVERPORT = 1313


class TwistedServer:
    def __init__(self, device):
        self.current_device = device
        self.connected = False

    def start_listening(self):
        reactor.listenTCP(SERVERPORT, DataReceiverFactory(self.current_device))
        reactor.run()


class DataReceiverFactory(ServerFactory):
    def __init__(self, device):
        self.current_device = device

    def buildProtocol(self, addr):
        print addr
        return DataReceiverServerProtocol(self.current_device)


class DataReceiverServerProtocol(Protocol, Observer):
    def update(self, data=None):
        processor = DataReceiver(data, self.current_device)
        self.try_to_perform_action(processor)
        self.transport.write("CLIENTID#BAXTER1\n")

    def __init__(self, device):
        self.current_device = device
        self.data_stream = DataStream()
        self.data_stream.register_observer(self)

    def dataReceived(self, data):
        self.data_stream.append(data)

    def connectionMade(self):
        print "Connection made"

    def connectionLost(self, reason):
        print 'Lost connection because {}'.format(reason)

    @staticmethod
    def try_to_perform_action(processor):
        try:
            processor.perform_action()
        except Exception, err:
            print err
