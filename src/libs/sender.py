import socket
from threading import Lock

PORT = 1314


class Sender(object):
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.connected = False
        self.lock_sending = Lock()

    def connect_to_server(self):
        self.connected = False
        print "Trying to connect to: ", PORT
        while not self.connected:
            try:
                self.clientsocket.connect(('127.0.0.1', PORT))
                self.connected = True
                print "Connected"
            except Exception as e:
               pass

    def send(self, message):
        if self.connected:
            self.lock_sending.acquire()
            self.clientsocket.send(message)
            self.lock_sending.release()
