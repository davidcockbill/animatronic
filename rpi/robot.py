#!/usr/bin/python3

import time
from led_panel import LedPanel
from button import Button
from sound import Sound
from cmd_proxy import CmdProxy
from head import Head
from eyes import Eyes
from face_tracker import FaceTracker
from actions import Actions
from utils import sleep_ms

class Robot:
    def __init__(self):
        self.standby = True
        self.led_panel = LedPanel()
        self.button = Button(self._button_pressed)
        self.sound = Sound()
        self.proxy = CmdProxy()
        self.head = Head(self.proxy)
        self.eyes = Eyes(self.proxy)
        self.tracker = FaceTracker(self.led_panel, self.sound, self.head, self.eyes)
        self.actions = Actions(self.head, self.eyes, self.sound)
        sleep_ms(500)

    def run(self):
        while True:
            try:
                if self.standby:
                    sleep_ms(250)
                else:
                    cpu_temperature = self._get_cpu_temperature()
                    if cpu_temperature < 80:
                        self.led_panel.pulse()
                        tracking = self.tracker.pulse()
                        if not tracking:
                            self.actions.pulse()
                    else:
                        print(f'Overheating: {cpu_temperature:.2f}')
                        self.led_panel.stop()
                        self.led_panel.red(True)
                        self.sound.no()
                        sleep_ms(5000)
            except KeyboardInterrupt:
                break 
        self.shutdown()

    def shutdown(self):
        print(f'\nShutting down')
        self.tracker.shutdown()
        self.led_panel.stop()

    def _toggle_standby(self):
        if self.standby:
            self.standby = False
        else:
            self.standby = True
        print(f'Standby: {self.standby}')

    def _button_pressed(self):
        print(f'temperature={self._get_cpu_temperature():.2f}C')
        self._toggle_standby()

    @staticmethod
    def _get_cpu_temperature():
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            cpu_temperature = temp_file.read()
        return float(cpu_temperature) / 1000


if __name__ == '__main__':
    Robot().run()
