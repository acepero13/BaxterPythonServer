from unittest import TestCase

from mock import MagicMock

from Server import Server
from src.customexceptions.CustomExceptions import ServerNotStartedException
import socket

class TestServer(TestCase):

    def setUp(self):
        self.server = Server(None)

    def tearDown(self):
        self.server.shut_down_connection()
        self.server.close_connection()

    def test_StartListeningWithConnectionParameters_isConnectedTrue(self):
        self.server.start_listening("localhost", 1313)
        result = self.server.is_listening()
        TestCase.assertEqual(self, result, True)

    def test_StartListeningWithoutConnectionParameters_isConnectedTrue(self):
        self.assertRaises(ServerNotStartedException, self.server.start_listening, "129.122.2.1", 1314)

    def test_Run_AcceptConnection_Connected(self):
        self.server.accept_new_connection = MagicMock(return_value=False)
        self.server.run()
        self.assertEqual(0, self.server.is_listening())

    def test_Run_AcceptSeveralClientConnections_Connected(self):
        self.server.start_listening("localhost", 1313)
        self.server.is_listening()
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






