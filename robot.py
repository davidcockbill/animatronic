#!/usr/bin/python3

from adafruit_servokit import ServoKit
import time
from head import Head
from eyes import Eyes
from actions import Actions
from utils import sleep_ms

class Robot:
    def __init__(self):
        self.kit = ServoKit(channels=16, address=0x44)
        self.head = Head(self.kit)
        self.eyes = Eyes(self.kit)
        self.actions = Actions(self.head, self.eyes)
        sleep_ms(500)

    def run(self):
        while True:
            try:
                self.actions.pulse()
            except KeyboardInterrupt:
                print(f'\nShutting down')
                self.actions.shutdown()
                break


if __name__ == '__main__':
    Robot().run()
