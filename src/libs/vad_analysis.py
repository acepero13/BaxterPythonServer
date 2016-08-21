import socket
from recorder import record
from recorder import OUTPUT_FILE
from src.libs.VAD import VAD

PORT = 1314
DURATION = 1
RUNNING = True

class VADAnalysis(object):
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        connected = False
        while not connected:
            try:
                self.clientsocket.connect(('127.0.0.1', PORT))
                connected = True
                print "Connected"
            except Exception as e:
               pass

    def start_listening(self):
        counter_instance = 0
        while RUNNING:
            record(DURATION)
            print "Calling moattar"
            speaking, AVERAGE_INTENSITY_OF_RUNS = VAD.moattar_homayounpour(OUTPUT_FILE, 0, counter_instance)
            counter_instance += 1
            print "Speaking: ", speaking
            if speaking:
                self.clientsocket.send("#DETECTEDSPEECH#end#\n")
            else:
                self.clientsocket.send("#NONDETECTEDSPEECH#end#\n")