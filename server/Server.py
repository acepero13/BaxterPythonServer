import socket
from threading import Thread

import thread

from Observer import Observer
from customexceptions.CustomExceptions import ServerNotStartedException


class Server(Thread, Observer):

    def __init__(self):
        Thread.__init__(self)
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_stream = None

    def update(self, obj=None):
        pass

    def start_listening(self, host="127.0.0.1", port=1313):
        try:
            self.socket.bind((host, port))
            self.socket.listen(5)
            self.setDaemon(True)
            self.start()
            self.connected = True
        except Exception, err:
            self.connected = False
            print err
            raise ServerNotStartedException

    def is_listening(self):
        return self.connected

    def close_connection(self):
        self.socket.close()

    def run(self):
        is_running = True
        while is_running:
            is_running = self.accept_new_connection()
        self.close_connection()
        self.shut_down_connection()

    def accept_new_connection(self):
        try:
            self.connected = False
            connection, address = self.socket.accept()
            thread.start_new_thread(self.handler, (connection, address))
            return True
        except socket.error, msg:
            print "Socket error! %s" % msg
            return False

    def shut_down_connection(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception, err:
            print err

    def process_received_data(self, data):
        pass



