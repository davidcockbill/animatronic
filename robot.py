#!/usr/bin/python3

from adafruit_servokit import ServoKit
import time
from head import Head
from eyes import Eyes
from face_detector import FaceDetector
from actions import Actions
from utils import sleep_ms, ms_timestamp

class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16, address=0x44)
        self.head = Head(self.kit)
        self.eyes = Eyes(self.kit)
        self.detector = FaceDetector()
        self.actions = Actions(self.head, self.eyes)
        self.last_face_sample = 0
        self.last_face_detected = 0
        self.face_tracking = True
        sleep_ms(500)

    def run(self):
        while True:
            try:
                self._process()
                self._pulse_delay()
            except KeyboardInterrupt:
                print(f'\nShutting down')
                self.detector.shutdown()
                self.actions.shutdown()
                break

    def _process_face(self):
        current_ms = ms_timestamp()
        sample_duration = current_ms - self.last_face_sample
        if sample_duration > 1000:
            face = self.detector.get_face()
            self.last_face_sample = current_ms
            if face is not None:
                if not self.face_tracking:
                    print(f'Tracking Face')
                self.face_tracking = True
                self.last_face_detected = current_ms
                x, y = face
                self.head.set(x, y)

            duration = current_ms - self.last_face_detected
            if duration > 2000:
                if self.face_tracking:
                    print(f'No Face')
                # self.face_tracking = False

    def _process(self):
        self._process_face()
        if self.face_tracking:
            self.head.pulse()
        else:
            no
            self.actions.pulse()


    @staticmethod
    def _pulse_delay():
        sleep_ms(0.00001)


if __name__ == '__main__':
    Robot().run()
