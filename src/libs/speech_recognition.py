import socket
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

CHUNK = 1024

modeldir = "/home/alvaro/Documents/Universitat/TesisProject/Libraries/SpeechRecognition-3.4.6/speech_recognition/pocketsphinx-data/en-US/acoustic-model"
datadir = "../../../test/data"

# Create a decoder with certain model
config = Decoder.default_config()
#config.set_string('-adcdev', 'sysdefault')
config.set_string('-hmm', '/mnt/data2/en-us-8khz/en')
config.set_string('-lm', '/mnt/data2/en-us-8khz/en-70k-0.1-pruned.lm')
config.set_string('-dict', '/mnt/data2/en-us-8khz/cmu07a.dic')
#config.set_string('-samprate', '8000')
config.set_string('-inmic', 'yes')
#config.set_string('-kws', 'command.list')


# Open file to read the data
#stream = open(os.path.join(datadir, "goforward.raw"), "rb")

# Alternatively you can read from microphone


def start_speech_server():

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    #while not connected:
    #    try:
    #        clientsocket.connect(('127.0.0.1', 1314))
    #        connected = True
    #    except Exception as e:
    #        print "Waiting for the server..."

    p = pyaudio.PyAudio()
    #print p.get_device_info_by_index(0)['defaultSampleRate']
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=CHUNK)
    stream.start_stream()
    # Process audio chunk by chunk. On keyword detected perform action and restart search
    decoder = Decoder(config)
    decoder.start_utt()

    while True:
        buf = stream.read(256, exception_on_overflow=False)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() != None:
            hypothesis = decoder.hyp()

            print("Word: ", decoder.hyp().hypstr)
            print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
            print ("Detected keyword, restarting search")
            #clientsocket.send("#DETECTEDSPEECH#end#\n")
            print "In speech: ", decoder.get_in_speech()
            decoder.end_utt()
            decoder.start_utt()


#
if __name__ == '__main__':
    start_speech_server()