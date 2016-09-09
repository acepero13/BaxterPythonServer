import cv2
#cascPath = sys.argv[1]
import math
cascPath = "/home/alvaro/ros_2/src/baxter_examples/scripts/src/libs/haarcascade_frontalface_default.xml"


class FaceDetector(object):
    def __init__(self, client_socket):
        self.sender = client_socket
        self.faceCascade = cv2.CascadeClassifier(cascPath)
        self.frame_width = 0
        self.frame_mid = 0
        self.get_frame_size()

    def execute(self):
        self.start_capturing()

    def get_frame_size(self):
        self.video_capture = cv2.VideoCapture(0)
        ret, frame = self.video_capture.read()
        self.frame_width = frame.shape[1]
        self.frame_mid = self.frame_width / 2

    def is_centered(self, x, w):
        ratio = 0
        diff = 0
        if self.frame_width > 0:
            ratio = w / float(self.frame_width)
            face_middle = (x + w / 2)
            diff = (self.frame_mid - face_middle) / float(self.frame_width)
        return math.fabs(diff) <= ratio, diff

    def start_capturing(self):
        while True:
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.get_faces(gray)
            self.paint_faces(faces, frame)
            #print "frame read"
            self.paint_video(frame)

        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

    def paint_video(self, frame):
        cv2.imshow('Video', frame)

    def paint_faces(self, faces, frame):
        for (x, y, w, h) in faces:
            color = (0, 0, 255)  # ed
            centered, diff = self.is_centered(x, w)
            if centered:
                print "Centered"
                color = (0, 255, 0)  # green
                self.sender.send("#FACECENTERED#" + str(diff) + "#end#\n")
            elif self.sender is not None:
                print "Non centered"
                self.sender.send("#FACENONCENTERED#" + str(diff) + "#end#\n")
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    def get_faces(self, gray):
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        return faces

if __name__ == '__main__':
    face_detector = FaceDetector(None)
    face_detector.start_capturing()