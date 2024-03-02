#!/usr/bin/python3

import cv2
from numpy import interp
from utils import sleep_ms
from imutils.video import VideoStream


class FaceDetector:
    def __init__(self):
        self.cascade_frontal = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cascade_profile = cv2.CascadeClassifier('haarcascade_profileface.xml')
        self.capture = VideoStream(usePiCamera=True).start()
        self.grayscale = True
        self.scale_factor = 1.3
        self.min_neighbors = 5
        sleep_ms(500)
        self.width, self.height = self._get_frame_size()

    def shutdown(self):
        print("Shutting down")
        self.capture.stop()
        cv2.destroyAllWindows()

    def get_face(self):
        frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if self.grayscale else frame

        faces = self._detect_frontal(frame)
        faces = self._detect_profile(frame) if not len(faces) else faces
        if len(faces): 
            return self._get_face(faces)

    def _get_frame_size(self):
        frame = self.capture.read()
        (height, width) = frame.shape[:2]
        return width, height

    def _detect_frontal(self, frame):
        return self.cascade_frontal.detectMultiScale(frame, scaleFactor=self.scale_factor, minNeighbors=self.min_neighbors)

    def _detect_profile(self, frame):
        return self.cascade_profile.detectMultiScale(frame, scaleFactor=self.scale_factor, minNeighbors=self.min_neighbors)

    def _scale_x(self, x):
        return round(interp(x,[0,self.width],[1.0,-1.0]), 4)

    def _scale_y(self, y):
        return round(interp(y,[0,self.height],[1.0,-1.0]), 4)

    def _get_face(self, faces):
        first_face = faces[0]
        (x, y, w, h) = first_face
        x_face = int(x + (w / 2.0))
        y_face = int(y + (h / 2.0))
        return self._scale_x(x_face), self._scale_y(y_face)


if __name__ == '__main__':
    detector = FaceDetector()

    print('Running..')
    while True:
        face = detector.get_face()
        if face is not None:
            x, y = face
            print(f'Face Detected x={x}, y={y}')
        sleep_ms(10)