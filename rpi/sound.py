#!/usr/bin/python3

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
        def wrapper(self) :
            self.pwm.start(50)
            func(self)
            self.pwm.stop()
        return wrapper

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
        

def main():
    sound = Sound()
    sound.hello()


if __name__ == '__main__':
    main()
