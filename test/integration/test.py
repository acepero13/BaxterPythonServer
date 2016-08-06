import socket


def test_Run_AcceptSeveralClientConnections_Connected():

        for i in range(2):
            client = create_client()
            client.send('Test')
            result = client.recv(1024)
            print result

def create_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 1313)
    sock.connect(server_address)
    return sock

if __name__ == '__main__':
    test_Run_AcceptSeveralClientConnections_Connected()