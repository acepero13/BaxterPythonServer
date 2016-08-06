import socket
from unittest import TestCase

from AsyncServer import TwistedServer


class TestServer(TestCase):
    def setUp(self):
        self.server = TwistedServer(None)

    def test_Run_AcceptSeveralClientConnections_Connected(self):

        for i in range(2):
            client = self.create_client()
            client.send('Test')
            result = client.recv(1024)
            self.assertEqual("CLIENTID#BAXTER1\n", result)

    @staticmethod
    def create_client():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 1313)
        sock.connect(server_address)
        return sock