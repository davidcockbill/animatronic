#!/usr/bin/python3

from face_detector import FaceDetector
from random import randrange
from utils import ms_timestamp

HEAD_SMOOTHER = 30

class FaceTracker:
    def __init__(self, sound, head, eyes):
        self.sound = sound
        self.head = head
        self.eyes = eyes
        self.detector = FaceDetector()
        self.last_face_detected = 0
        self.face_tracking = False
        self.blink_timestamp = self._blink_timestamp()

        self.previous_x = 1000
        self.previous_y = 1000

    def shutdown(self):
        self.detector.shutdown()

    def pulse(self):
        self._blink()
        current_ms = ms_timestamp()
        face = self.detector.get_face()
        if face is not None:
            self.last_face_detected = current_ms
            if not self.face_tracking:
                print(f'Tracking Face')
                self.sound.hello()
                self.face_tracking = True
                self.eyes.wide_eyes()
                self.previous_x = 1000
                self.previous_y = 1000
            x, y = face
            # print(f'x={x}, y={y}')

            if abs(self.previous_x - x) > HEAD_SMOOTHER:
                self.head.set_x_position(x)
            self.eyes.set_x_position(x)

            if abs(self.previous_y - y) > HEAD_SMOOTHER:
                self.head.set_y_position(y)
            self.eyes.set_y_position(y)

            self.previous_x = x
            self.previous_y = y

        duration = current_ms - self.last_face_detected
        if duration > 2000:
            if self.face_tracking:
                print(f'No Face')
                self.face_tracking = False
                self.head.face_ahead()
                self.eyes.default_eyes()


    @staticmethod
    def _blink_timestamp():
        return ms_timestamp() + randrange(5000, 15000)

    def _blink(self):
        if ms_timestamp() > self.blink_timestamp:
            self.eyes.blink()
            self.blink_timestamp = self._blink_timestamp()


if __name__ == '__main__':
    tracker = FaceTracker()
