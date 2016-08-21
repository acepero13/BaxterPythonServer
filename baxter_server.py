import sys
from threading import Thread

from src.libs.vad_analysis import VADAnalysis
from src.server.AsyncServer import TwistedServer
from src.plugindevices.ImageViewerDevice import ImageViewerDevice
from src.libs.speech_recognition import *
from src.server.Server import Server
#import head_gestures


def start_speech_recognition_server():
    server_vad = VADAnalysis()
    thread_speech = Thread(target=server_vad.start_listening, args=())
    thread_speech.start()
    return thread_speech


def start_thread_server(device):
    server = TwistedServer(device)
    thread_listener = Thread(target=server.start_listening, args=())
    thread_listener.start()
    return thread_listener


if __name__ == '__main__':
    print(sys.path)
    #device = head_gestures.HeadGestures()
    device = ImageViewerDevice()
    thread_listener = start_thread_server(device)
    thread_speech = start_speech_recognition_server()
    thread_listener.join()
    thread_speech.join()
    print "Exit"
