import sys
from threading import Thread

from src.libs.face_detection import FaceDetector
from src.libs.sender import Sender
from src.libs.sentimentanalysis.sentiment_analysis import SentimentServer
from src.libs.vad_analysis import VADAnalysis
from src.server.AsyncServer import TwistedServer
from src.plugindevices.ImageViewerDevice import ImageViewerDevice
#import head_gestures


def start_speech_recognition_server(sender):
    server_vad = VADAnalysis(sender)
    thread_speech = Thread(target=server_vad.execute, args=())
    thread_speech.start()
    return thread_speech

def start_speech_face_detection(sender):
    face_detector = FaceDetector(sender)
    thread_face = Thread(target=face_detector.execute, args=())
    thread_face.start()
    return thread_face


def start_thread_server(device):
    server = TwistedServer(device)
    thread_listener = Thread(target=server.start_listening, args=())
    thread_listener.start()
    return thread_listener


def start_sentiment_analisys():
    sentimentServer = SentimentServer()
    thread_sentiment = Thread(target=sentimentServer.start_server, args=())
    thread_sentiment.start()
    return  thread_sentiment


if __name__ == '__main__':
    #asdb.set_trace()
    #device = head_gestures.HeadGestures()
    device = ImageViewerDevice()
    thread_listener = start_thread_server(device)
    thread_sentiment_analysis = start_sentiment_analisys()
    thread_listener.join()
    thread_sentiment_analysis.join()

    #sender = Sender()
    #thread_speech = start_speech_recognition_server(sender)
    #thread_face_detector = start_speech_face_detection(sender)

    #thread_speech.join()
    #thread_face_detector.join()
    print "Exit"
