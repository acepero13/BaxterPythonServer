# wx_ipc.py
import select
import socket
import wx

from threading import Thread

########################################################################

from src.server.Server import Server
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher




class MyPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.PhotoMaxSize = 240

        self.createWidgets()

        Publisher.subscribe(self.updateDisplay, "update")

    def createWidgets(self):
        instructions = 'Browse for an image'
        img = wx.EmptyImage(640, 480)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                         wx.BitmapFromImage(img))


        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)


        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.SetSizer(self.mainSizer)

        self.Layout()
 
    #----------------------------------------------------------------------

    def onView(self, data):
        #filepath = self.photoTxt.GetValue()
        img = wx.ImageFromStream(data)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(W,H)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.Refresh()
    #----------------------------------------------------------------------
    def updateDisplay(self, msg):
        """
        Display what was sent via the socket server
        """
        if msg and msg.data:
            self.onView(msg.data)

 
########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Communication Demo")
        panel = MyPanel(self)
 
        # start the IPC server
        #self.server = Server()
        #self.server.start_listening()

        self.Show()
 
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()