import socket
from threading import Lock

import time
from src.constants.constants import *


class Sender(object):
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.lock_sending = Lock()
        self.connect_to_server()

    def connect_to_server(self):
        self.connected = False
        print "Trying to connect to: ", VSM_SERVER_PORT
        while not self.connected:
            try:
                self.clientsocket.connect(('127.0.0.1', VSM_SERVER_PORT))
                self.connected = True
                print "Connected"
                time.sleep(WAITINGTIME)
            except Exception as e:
               pass

    def send(self, message):
        if self.connected:
            self.lock_sending.acquire()
            print "sending " + message
            self.clientsocket.send(message)
            self.lock_sending.release()
