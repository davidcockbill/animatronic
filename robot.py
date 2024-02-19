#!/usr/bin/python3

from adafruit_servokit import ServoKit
import time
from head import Head
from eyes import Eyes
from face_tracker import FaceTracker
from actions import Actions
from utils import sleep_ms

class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16, address=0x44)
        self.head = Head(self.kit)
        self.eyes = Eyes(self.kit)
        self.tracker = FaceTracker(self.head, self.eyes)
        self.actions = Actions(self.head, self.eyes)
        sleep_ms(500)

    def run(self):
        while True:
            try:
                # self.run_actions()
                self.tracker.pulse()
            except KeyboardInterrupt:
                print(f'\nShutting down')
                self.tracker.shutdown()
                self.actions.shutdown()
                break 

    def run_actions(self):
        self.actions.pulse()
        # self._pulse_delay()

    @staticmethod
    def _pulse_delay():
        sleep_ms(0.000001)


if __name__ == '__main__':
    Robot().run()
