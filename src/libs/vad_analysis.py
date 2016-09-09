import socket
from recorder import record
from recorder import OUTPUT_FILE
from src.libs.VAD import VAD
from src.libs.sender import Sender

SILENCE_THRESHOLD = 5


DURATION = 1
RUNNING = True

class VADAnalysis(object):
    def __init__(self, client):
        self.sender = client
        self.counter_no_speaking = 0

    def execute(self):
        self.start_listening()

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
            self.sender.send("#DETECTEDSPEECH#end#\n")
            self.counter_no_speaking = 0
        else:
            self.counter_no_speaking += 1
            if self.counter_no_speaking >= SILENCE_THRESHOLD:
                self.sender.send("#NONDETECTEDSPEECH#end#\n")