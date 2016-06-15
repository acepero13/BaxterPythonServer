import StringIO
import base64

from wx import wx
from wx.lib.pubsub import Publisher

from src.server.GenericDevice import GenericDevice


class ImageViewerDevice(GenericDevice):
    def __init__(self):
        self.data = None

    def paint(self, params):
        if len(params) > 0:
            return self.send_image_to_wx(params)
        return False

    @staticmethod
    def send_image_to_wx(params):
        img = params[0]
        image_data = base64.b64decode(img)
        sbuf = StringIO.StringIO(image_data)
        wx.CallAfter(Publisher().sendMessage, "update", sbuf)
        return True
