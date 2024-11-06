#!/usr/bin/python3

import RPi.GPIO as GPIO
 

class LedPanel:
    def __init__(self):
        self.red_pin = 22
        self.green_pin = 16
        self.blue_pin = 18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        self.reset()

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

    def _set(self, pin, on):
        value = GPIO.HIGH if on else GPIO.LOW
        GPIO.output(pin, value)


def main():
    panel = LedPanel()
    panel.red(False)
    panel.green(True)
    panel.blue(False)


if __name__ == '__main__':
    main()