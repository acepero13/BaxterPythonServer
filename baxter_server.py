from AsyncServer import TwistedServer
from src.plugindevices.ImageViewerDevice import ImageViewerDevice
from src.server.Server import Server
#import head_gestures
if __name__ == '__main__':
    #device = head_gestures.HeadGestures()
    device = ImageViewerDevice()
    server = TwistedServer(device)
    server.start_listening()
    #while 1:
    #    pass
