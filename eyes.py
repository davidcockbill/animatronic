#!/usr/bin/python3

from adafruit_servokit import ServoKit
from servo import Servo, Smoothed_Servo
from utils import sleep_ms

LEFT_EYE_X_SERVO = 0
LEFT_EYE_Y_SERVO = 1
RIGHT_EYE_X_SERVO = 2
RIGHT_EYE_Y_SERVO = 3
EYE_LID_SERVO = 4


class Eyes:
    def __init__(self, kit):
        print(f'Initialising Eyes ...')
        self.kit = kit

        self.left_eye_x = Smoothed_Servo(kit, LEFT_EYE_X_SERVO, 0.47, 0.2)
        self.left_eye_y = Smoothed_Servo(kit, LEFT_EYE_Y_SERVO, 0.55, 0.13)
        self.right_eye_x = Smoothed_Servo(kit, RIGHT_EYE_X_SERVO, 0.48, 0.2)
        self.right_eye_y = Smoothed_Servo(kit, RIGHT_EYE_Y_SERVO, 0.57, 0.13, servo_reversed=True)

        self.lid = Servo(kit, EYE_LID_SERVO, 0.5, 0.4)

        self.smoothed_servos = [self.left_eye_x, self.left_eye_y, self.right_eye_x, self.right_eye_y]
        self.all_servos = [self.left_eye_x, self.left_eye_y, self.right_eye_x, self.right_eye_y, self.lid]

        print(f'Initialised Eyes')

    def reset(self):
        [servo.reset() for servo in self.all_servos]

    def pulse(self):
        return all([servo.pulse() for servo in self.smoothed_servos])

    def slow(self):
        [servo.slow() for servo in self.smoothed_servos]

    def fast(self):
        [servo.fast() for servo in self.smoothed_servos]

    def default_eyes(self):
        print(f'Defaulting ...')
        self.look_ahead()
        # self.open_eyes()
        print(f'Defaulted')

    def look_ahead(self):
        print(f'Look ahead')
        self.left_eye_x.centre()
        self.left_eye_y.centre()

        self.right_eye_x.centre()
        self.right_eye_y.centre()

    def look_left(self):
        print(f'Look left')
        self.left_eye_x.position(1)
        self.right_eye_x.position(1)

    def look_right(self):
        print(f'Look right')
        self.left_eye_x.position(-1)
        self.right_eye_x.position(-1)

    def cross_eyed(self):
        print(f'Cross eyed')
        self.left_eye_x.position(-1)
        self.right_eye_x.position(1)

    def look_up(self):
        print(f'Look up')
        self.left_eye_y.position(1)
        self.right_eye_y.position(1)

    def look_down(self):
        print(f'Look down')
        self.left_eye_y.position(-1)
        self.right_eye_y.position(-1)

    def close_eyes(self):
        self.lid.position(-1)

    def open_eyes(self):
        self.lid.centre()

    def full_open_eyes(self):
        self.lid.position(1)

    def blink(self):
        self.close_eyes()
        sleep_ms(200)
        self.open_eyes()


if __name__ == '__main__':
    kit = ServoKit(channels=16, address=0x44)
    eyes = Eyes(kit)

    def run(action):
        action()
        while not eyes.pulse():
            sleep_ms(10)

    # actions
    run(eyes.look_ahead)
    run(eyes.cross_eyed)
    # run(eyes.blink)
    # run(eyes.look_right)
    # run(eyes.look_ahead)
    # run(eyes.blink)
    # run(eyes.look_left)
    # run(eyes.blink)

    run(eyes.look_ahead)
