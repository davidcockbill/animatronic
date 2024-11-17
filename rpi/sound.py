#!/usr/bin/python3

import functools
import RPi.GPIO as GPIO
from utils import sleep_ms
 

class Sound:
    def __init__(self):
        self.pin = 37
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 100)

    def play(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            self.pwm.start(50)
            func(self, *args, **kwargs)
            self.pwm.stop()
        return wrap

    @play
    def hello(self, delay=0.5):
        frequency = 100
        for i in range(100):
            self.pwm.ChangeFrequency(frequency)
            frequency += 5
            sleep_ms(delay)

        for i in range(100):
            self.pwm.ChangeFrequency(frequency)
            frequency -= 2
            sleep_ms(delay)
        
        for i in range(100):
            self.pwm.ChangeFrequency(frequency)
            frequency += 5
            sleep_ms(delay)

    @play
    def chirp(self):
        self.pwm.ChangeFrequency(900)
        sleep_ms(50)
        self.pwm.ChangeFrequency(1300)
        sleep_ms(50)
        self.pwm.ChangeFrequency(1700)
        sleep_ms(50)

    @play
    def warble(self):
        frequency = 1000
        duration = 20
        step = 30
        for i in range(2):
            self.pwm.ChangeFrequency(frequency)
            sleep_ms(duration)
            frequency += step
            self.pwm.ChangeFrequency(frequency)
            sleep_ms(duration)
            frequency -= step
            self.pwm.ChangeFrequency(frequency)
            sleep_ms(duration)
            frequency -= step
            self.pwm.ChangeFrequency(frequency)
            sleep_ms(duration)
            frequency += step

    @play
    def no(self):
        self.pwm.ChangeFrequency(60)
        sleep_ms(100)
        self.pwm.ChangeFrequency(20)
        sleep_ms(200)

    @play
    def raspberry(self):
        self.pwm.ChangeFrequency(20)
        sleep_ms(300)


def main():
    sound = Sound()
    sound.no()


if __name__ == '__main__':
    main()
