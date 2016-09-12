import cv2
#cascPath = sys.argv[1]
import math
from src.constants.constants import *
import time
is_from_main = False

class FaceDetector(object):
    def __init__(self, client_socket):
        self.sender = client_socket
        self.faceCascade = cv2.CascadeClassifier(CASCPATH)
        self.frame_width = 0
        self.frame_mid = 0
        self.get_frame_size()

    def execute(self):
        self.start_capturing()

    def get_frame_size(self):
        self.video_capture = cv2.VideoCapture(VIDEO_CAMERA)
        self.set_resolution()
        ret, frame = self.video_capture.read()
        self.frame_width = frame.shape[WIDTH]
        self.frame_mid = self.frame_width / 2

    def set_resolution(self):
        self.video_capture.set(3, 640)
        self.video_capture.set(4, 480)

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
            self.process_faces(faces, frame)
            time.sleep(WAITINGTIME)
            if is_from_main:
                self.paint_video(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

    def process_faces(self, faces, frame):
        if faces is not None and len(faces):
            self.paint_faces(faces, frame)
        elif self.sender is not None:  # TODO: Hacer panning
            self.send_to_server("#FACENONCENTERED#" + str(0) + "#end#\n")

    def paint_video(self, frame):
        cv2.imshow('Video', frame)

    def paint_faces(self, faces, frame):
        for (x, y, w, h) in faces:
            color = (0, 0, 255)  # ed
            centered, diff = self.is_centered(x, w)
            if centered:
                color = (0, 255, 0)  # green
                self.send_to_server("#FACECENTERED#" + str(diff) + "#end#\n")
            elif self.sender is not None:
                self.send_to_server("#FACENONCENTERED#" + str(diff) + "#end#\n")
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    def send_to_server(self, message):
        if self.sender is not None:
            self.sender.send(message)


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
    is_from_main = True
    face_detector = FaceDetector(None)
    face_detector.start_capturing()