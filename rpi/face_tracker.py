#!/usr/bin/python3

from face_detector import FaceDetector
from random import randrange
from utils import ms_timestamp

HEAD_SMOOTHER = 100

class FaceTracker:
    def __init__(self, led_panel, sound, head, eyes):
        self.led_panel = led_panel
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
            self.led_panel.blue(True)
            self.last_face_detected = current_ms
            if not self.face_tracking:
                self._start_tracking()
            x, y = face
            # print(f'x={x}, y={y}')

            lids_position = 1500 if (x > 1100) else 1000
            self.eyes.set_lids_position(lids_position)


            if abs(self.previous_x - x) > HEAD_SMOOTHER:
                self.head.set_x_position(x)
            self.eyes.set_x_position(x)

            if abs(self.previous_y - y) > HEAD_SMOOTHER:
                self.head.set_y_position(y)
            self.eyes.set_y_position(y)

            self.previous_x = x
            self.previous_y = y
        else:
            self.led_panel.blue(False)

        duration = current_ms - self.last_face_detected
        if duration > 2000:
            if self.face_tracking:
                self._stop_tracking()

    def _start_tracking(self):
        print(f'Tracking Face')
        self.led_panel.green(True)
        self.sound.chirp()
        self.face_tracking = True
        self.eyes.wide_eyes()
        self.previous_x = 1000
        self.previous_y = 1000

    def _stop_tracking(self):
        print(f'No Face')
        self.led_panel.green(False)
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
