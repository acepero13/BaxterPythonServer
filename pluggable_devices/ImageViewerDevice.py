from GenericDevice import GenericDevice


class ImageViewerDevice(GenericDevice):
    def __init__(self):
        self.data = None

    def paint(self):
        print "I'm paiting"
