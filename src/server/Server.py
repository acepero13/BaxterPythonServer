import socket
import thread
from threading import Thread


from DataStream import DataStream
from Observer import Observer
from src.customexceptions.CustomExceptions import ServerNotStartedException
from src.plugindevices.ImageViewerDevice import ImageViewerDevice
from src.utils.datareceiver import DataReceiver

BROKEN_PIPE = 32


class Server(Thread, Observer):

    def __init__(self):
        Thread.__init__(self)
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def update(self, data=None):
        img_device = ImageViewerDevice()
        processor = DataReceiver(data, img_device)
        result = processor.perform_action()
        self.send_response(self.connection)

    def start_listening(self, host="127.0.0.1", port=1313):
        try:
            self.socket.bind((host, port))
            self.socket.listen(5)
            self.setDaemon(True)
            self.start()
            self.connected = True
            print "listening in address: ", host, " in port: ", port
        except Exception, err:
            self.connected = False
            print err
            raise ServerNotStartedException

    def is_listening(self):
        return self.connected

    def close_connection(self):
        self.socket.close()

    def handler(self, connection, addr):
        data_stream = DataStream()
        data_stream.register_observer(self)
        is_alive = True
        while is_alive:
            is_alive = self.read_data(connection, data_stream)

    def read_data(self, connection, data_stream):
        data = connection.recv(1024)
        if not data:
            self.connected = False
            connection.close()
            return False
        else:
            data_stream.append(data)
            return True

    def run(self):
        is_running = True
        while is_running:
            is_running = self.accept_new_connection()
        self.close_connection()
        self.shut_down_connection()

    def accept_new_connection(self):
        try:
            self.connected = False
            self.connection, address = self.socket.accept()
            thread.start_new_thread(self.handler, (self.connection, address))
            return True
        except socket.error, msg:
            print "Socket error! %s" % msg
            return False

    def shut_down_connection(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception, err:
            print err

    def send_response(self, connection):
        try:
            connection.sendall("CLIENTID#BAXTER1\n")
            return True
        except socket.error, e:
            print "Error enviando", e
            self.process_error_sending_response(connection, e)
            print "Cannot send back"

    def process_error_sending_response(self, connection, e):
        if e.errno == BROKEN_PIPE:
            self.connected = False
            self.connect_client()
            try:
                connection.sendall("CLIENTID#BAXTER1\n")
            except socket.error, e:
                return False



