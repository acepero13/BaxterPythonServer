import StringIO
import base64

from wx import wx
from wx.lib.pubsub import Publisher
from threading import Thread
from imageviwer import MyFrame
from src.server.GenericDevice import GenericDevice

import logging
logging.basicConfig(filename='ImageViewerLog.log',level=logging.DEBUG)
class ImageViewerDevice(GenericDevice, Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data = None
        self.start()

    def paint(self, params):
        if len(params) > 0:
            logging.info('Im paiting an image!')
            return self.send_image_to_wx(params)
        return False

    def look_left(self):
        print "I'm looking left!"
        logging.info('Im looking left!!')

    def look_at(self, params):
        at = params[0]
        print "I'm looking at: " + at
        logging.info("I'm looking at: " + at)


    @staticmethod
    def send_image_to_wx(params):
        img = params[0]
        image_data = base64.b64decode(img)
        sbuf = StringIO.StringIO(image_data)
        wx.CallAfter(Publisher().sendMessage, "update", sbuf)
        return True

    def run(self):
        self.app = wx.App(False)
        frame = MyFrame()
        self.app.MainLoop()



