import socket

from src.libs.sentimentanalysis.command_parser import CommandParser
from src.libs.sentimentanalysis.textanalysis import SentimentClassifier

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
class SentimentServer(object):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        print "Server started"
        print "Port: ", UDP_PORT
        self.commandParser = CommandParser()
        self.textAnalysis = SentimentClassifier(None, "/home/alvaro/Documents/Universitat/TesisProject/Python/BaxterPythonServer/training.csv")

    def start_server(self):
        self.listen()


    def listen(self):
        self.sock.bind((UDP_IP, UDP_PORT))
        self.receive()

    def receive(self):
        print "Listening..."
        while True:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.commandParser.parse(data)
            message = self.commandParser.getMessage()
            if message != "":
                classification = self.textAnalysis.classify(message)
                print message + " is: " +classification
                print "\n"
            #print "received message:", data


