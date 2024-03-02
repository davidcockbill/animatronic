#!/usr/bin/python3

from face_detector import FaceDetector
from random import randrange
from utils import ms_timestamp

SAMPLE_THROTTLE = 1000

class FaceTracker:
    def __init__(self, head, eyes):
        self.head = head
        self.eyes = eyes
        self.detector = FaceDetector()
        self.last_face_sample = 0
        self.last_face_detected = 0
        self.face_tracking = False
        self.blink_timestamp = self._blink_timestamp()

    def shutdown(self):
        self.detector.shutdown()

    def pulse(self):
        self._blink()
        current_ms = ms_timestamp()
        last_sample_duration = current_ms - self.last_face_sample
        if last_sample_duration > SAMPLE_THROTTLE:
            face = self.detector.get_face()
            self.last_face_sample = current_ms
            if face is not None:
                if not self.face_tracking:
                    print(f'Tracking Face')
                    self.face_tracking = True
                self.last_face_detected = current_ms
                x, y = face
                # if abs(x) < 0.5:
                #     self.head.set_x(x/2)
                # self.eyes.set_x(x)

                # if abs(y) > 0.5:
                #     self.head.set_y(y/2)
                # self.eyes.set_y(y)

            duration = current_ms - self.last_face_detected
            if duration > 2000:
                if self.face_tracking:
                    print(f'No Face')
                    self.face_tracking = False
        # self.head.pulse()
        # self.eyes.pulse()

    @staticmethod
    def _blink_timestamp():
        return ms_timestamp() + randrange(5000, 15000)

    def _blink(self):
        if ms_timestamp() > self.blink_timestamp:
            self.eyes.blink()
            self.blink_timestamp = self._blink_timestamp()


if __name__ == '__main__':
    tracker = FaceTracker()
