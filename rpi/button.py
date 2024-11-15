#!/usr/bin/python3

import RPi.GPIO as GPIO


class Button:
    def __init__(self, callback):
        self.pin = 36
        self.callback = callback
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.button_pressed, bouncetime=200)


    def button_pressed(self, channel):
        if channel == self.pin:
            self.callback()

def main():
    button = Button()
    while True:
        pass
            

if __name__ == '__main__':
    main()