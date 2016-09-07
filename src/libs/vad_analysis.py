import socket
from recorder import record
from recorder import OUTPUT_FILE
from src.libs.VAD import VAD

SILENCE_THRESHOLD = 5

PORT = 1314
DURATION = 1
RUNNING = True

class VADAnalysis(object):
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.counter_no_speaking = 0

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
            try:
                record(DURATION)
                self.analyse(counter_instance)
            except IOError as err:
                continue

    def analyse(self, counter_instance):
        print "Calling moattar"
        speaking, AVERAGE_INTENSITY_OF_RUNS = VAD.moattar_homayounpour(OUTPUT_FILE, 0, counter_instance)
        counter_instance += 1
        print "Speaking: ", speaking
        if speaking:
            self.clientsocket.send("#DETECTEDSPEECH#end#\n")
            self.counter_no_speaking = 0
        else:
            self.counter_no_speaking += 1
            if self.counter_no_speaking >= SILENCE_THRESHOLD:
                self.clientsocket.send("#NONDETECTEDSPEECH#end#\n")