#!/usr/bin/python3

import time
from led_panel import LedPanel
from sound import Sound
from cmd_proxy import CmdProxy
from head import Head
from eyes import Eyes
from face_tracker import FaceTracker
from actions import Actions
from utils import sleep_ms
# from gpiozero import CPUTemperature

class Robot:
    def __init__(self):
        self.led_panel = LedPanel()
        self.sound = Sound()
        self.proxy = CmdProxy()
        self.head = Head(self.proxy)
        self.eyes = Eyes(self.proxy)
        self.tracker = FaceTracker(self.led_panel, self.sound, self.head, self.eyes)
        # self.actions = Actions(self.head, self.eyes)
        sleep_ms(500)

    def run(self):
        while True:
            try:

                # cpu_temperature = CPUTemperature().temperature
                cpu_temperature = 50

                if cpu_temperature < 70:
                    # self.run_actions()
                    self.tracker.pulse()
                    # self._pulse_delay()
            except KeyboardInterrupt:
                print(f'\nShutting down')
                self.tracker.shutdown()
                # self.actions.shutdown()
                break 

    def run_actions(self):
        self.actions.pulse()
        self._pulse_delay()

    @staticmethod
    def _pulse_delay():
        sleep_ms(1)


if __name__ == '__main__':
    Robot().run()
