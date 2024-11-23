#!/usr/bin/python3

from context import Context
from button import Button
from face_tracker import FaceTracker
from actions import SleeperActions
from utils import sleep_ms, get_cpu_temperature

class Robot:
    def __init__(self):
        self.standby = True
        self.context = Context()
        self.button = Button(self._button_pressed)
        self.tracker = FaceTracker(self.context)
        self.actions = SleeperActions(self.context)
        self.context.led_panel.red_flash()
        sleep_ms(500)

    def run(self):
        while True:
            try:
                if self.standby:
                    self.context.led_panel.pulse()
                else:
                    cpu_temperature = get_cpu_temperature()
                    if cpu_temperature < 80:
                        self.context.led_panel.pulse()
                        tracking = self.tracker.pulse()
                        if not tracking:
                            self.actions.pulse()
                    else:
                        print(f'Overheating: {cpu_temperature:.2f}')
                        self.context.led_panel.stop()
                        self.context.led_panel.red(True)
                        self.context.sound.no()
                        sleep_ms(5000)
            except KeyboardInterrupt:
                break 
        self.shutdown()

    def shutdown(self):
        print(f'\nShutting down')
        self.tracker.shutdown()
        self.context.led_panel.stop()

    def _toggle_standby(self):
        if self.standby:
            self.context.led_panel.scan()
            self.standby = False
        else:
            self.context.led_panel.red_flash()
            self.standby = True
        print(f'Standby: {self.standby}')

    def _button_pressed(self):
        print(f'temperature={get_cpu_temperature():.2f}C')
        self._toggle_standby()


if __name__ == '__main__':
    Robot().run()
