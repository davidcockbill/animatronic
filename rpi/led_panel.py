#!/usr/bin/python3

import RPi.GPIO as GPIO
from utils import ms_timestamp, sleep_ms

UPDATE_DURATION = 200

class LedPanel:
    def __init__(self):
        self.red_pin = 16
        self.green_pin = 18
        self.blue_pin = 22
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

        self.next_update = ms_timestamp()
        self.animation = []
        self.animation_idx = 0
        self.reset()

    def pulse(self):
        current = ms_timestamp()
        if current > self.next_update:
            self._animate()
            self.next_update = current + UPDATE_DURATION

    def reset(self):
        self.red(False)
        self.green(False)
        self.blue(False)

    def red(self, on):
        self._set(self.red_pin, on)

    def green(self, on):
        self._set(self.green_pin, on)

    def blue(self, on):
        self._set(self.blue_pin, on)

    def scan(self):
        self.animation_idx = 0
        self.animation = [
            [(self.red, True), (self.green, False), (self.blue, False)],
            [(self.red, False), (self.green, True), (self.blue, False)],
            [(self.red, False), (self.green, False), (self.blue, True)],
            [(self.red, False), (self.green, True), (self.blue, False)],
        ]
        self._animate()

    def red_flash(self):
        self.animation_idx = 0
        self.animation = [
            [(self.red, True), (self.green, False), (self.blue, False)],
            [(self.red, False), (self.green, False), (self.blue, False)],
        ]
        self._animate()

    def stop(self):
        self.animation = []
        self.animation_idx = 0
        self.reset()

    def _set(self, pin, on):
        value = GPIO.HIGH if on else GPIO.LOW
        GPIO.output(pin, value)

    def _animate(self):
        if len(self.animation):
            frame = self.animation[self.animation_idx]
            for function, state in frame:
                function(state)

            self.animation_idx += 1
            self.animation_idx %= len(self.animation)


def main():
    panel = LedPanel()
    panel.scan()
    for i in range(100):
        panel.pulse()
        sleep_ms(100)
    panel.stop()
    panel.red(True)


if __name__ == '__main__':
    main()