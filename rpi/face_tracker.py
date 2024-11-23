#!/usr/bin/python3

from face_detector import FaceDetector
from random import randrange
from utils import ms_timestamp
from context import Context

HEAD_SMOOTHER = 100
CHECK_TIME = 500

class FaceTracker:
    def __init__(self, context):
        self.led_panel = context.led_panel
        self.sound = context.sound
        self.head = context.head
        self.eyes = context.eyes
        self.detector = FaceDetector(context.capture)
        self.next_check_ms = 0
        self.last_face_detected = 0
        self.face_tracking = False
        self.blink_timestamp = self._blink_timestamp()

        self.previous_x = 1000
        self.previous_y = 1000

        self.led_panel.scan()

    def shutdown(self):
        self.detector.shutdown()

    def pulse(self):
        self._blink()
        current_ms = ms_timestamp()
        if self.face_tracking or current_ms > self.next_check_ms:
            self.next_check_ms = current_ms + CHECK_TIME
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
        return self.face_tracking

    def _start_tracking(self):
        print(f'Tracking Face')
        self.led_panel.stop()
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
        self.led_panel.scan()

    @staticmethod
    def _blink_timestamp():
        return ms_timestamp() + randrange(5000, 15000)

    def _blink(self):
        if ms_timestamp() > self.blink_timestamp:
            self.eyes.blink()
            self.blink_timestamp = self._blink_timestamp()


if __name__ == '__main__':
    context = Context()
    tracker = FaceTracker(context)
