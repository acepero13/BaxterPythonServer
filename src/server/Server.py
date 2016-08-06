import socket
import thread
from threading import Thread


from DataStream import DataStream
from Observer import Observer
from src.customexceptions.CustomExceptions import ServerNotStartedException
from src.utils.datareceiver import DataReceiver

BROKEN_PIPE = 32


class Server(Thread, Observer):

    def __init__(self, device):
        Thread.__init__(self)
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.current_device = device

    # Override
    def update(self, data=None):
        processor = DataReceiver(data, self.current_device)
        self.try_to_perform_action(processor)
        self.send_response(self.connection)

    @staticmethod
    def try_to_perform_action(processor):
        try:
            processor.perform_action()
        except Exception, err:
            print err

    def start_listening(self, host="127.0.0.1", port=1313):
        try:
            self.bind_and_start(host, port)
            print "listening in address: ", host, " in port: ", port
        except Exception, err:
            self.connected = False
            print err
            raise ServerNotStartedException

    def bind_and_start(self, host, port):
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.setDaemon(True)
        self.start()
        self.connected = True

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
            return self.close_client_connection(connection)
        else:
            data_stream.append(data)
            return True

    def close_client_connection(self, connection):
        self.connected = False
        connection.close()
        return False

    def run(self):
        is_running = True
        while is_running:
            is_running = self.accept_new_connection()
        self.shut_down_connection()
        self.close_connection()

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
