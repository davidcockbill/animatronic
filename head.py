#!/usr/bin/python3

from adafruit_servokit import ServoKit
from servo import Smoothed_Servo
from utils import sleep_ms

ROTATION_SERVO = 8
RIGHT_SERVO = 9
LEFT_SERVO = 10


class Head:
    def __init__(self, kit):
        print(f'Initialising Head ...')
        self.kit = kit

        self.rotation_servo = Smoothed_Servo(kit, ROTATION_SERVO, 0.5, 0.2)
        self.right_servo = Smoothed_Servo(kit, RIGHT_SERVO, 0.5, 0.25, servo_reversed=True)
        self.left_servo = Smoothed_Servo(kit, LEFT_SERVO, 0.5, 0.25)

        self.smoothed_servos = [self.rotation_servo, self.right_servo, self.left_servo]
        print(f'Initialised Head')

    def reset(self):
        [servo.reset() for servo in self.smoothed_servos]

    def pulse(self):
        return all([servo.pulse() for servo in self.smoothed_servos])

    def slow(self):
        [servo.slow() for servo in self.smoothed_servos]

    def fast(self):
        [servo.fast() for servo in self.smoothed_servos]

    def face_ahead(self):
        print(f'Face ahead')
        self.face_middle()
        self.face_level()

    def face_left(self):
        print(f'Face left')
        self.rotation_servo.position(1.0)

    def face_middle(self):
        print(f'Face middle')
        self.rotation_servo.centre()

    def face_right(self):
        print(f'Face right')
        self.rotation_servo.position(-1.0)

    def face_up(self):
        print(f'Face up')
        self.left_servo.position(1.0)
        self.right_servo.position(1.0)

    def face_level(self):
        print(f'Face level')
        self.right_servo.centre()
        self.left_servo.centre()

    def face_down(self):
        print(f'Face down')
        self.left_servo.position(-1.0)
        self.right_servo.position(-1.0)

    def tilt_left(self):
        print(f'Tilt left')
        self.left_servo.position(1.0)
        self.right_servo.position(-1.0)

    def tilt_right(self):
        print(f'Tilt right')
        self.left_servo.position(-1.0)
        self.right_servo.position(1.0)


if __name__ == '__main__':
    kit = ServoKit(channels=16, address=0x44)
    head = Head(kit)

    def run(action):
        action()
        while not head.pulse():
            sleep_ms(1)

    # actions
    # run(head.tilt_left)
    # run(head.face_ahead)
    # run(head.tilt_right)
    # run(head.face_ahead)

    # run(head.face_left)
    # run(head.face_ahead)
    # run(head.face_right)
    # run(head.face_ahead)

    run(head.slow)
    run(head.face_left)
    run(head.face_down)
    run(head.face_middle)
    run(head.face_right)
    run(head.face_level)

    run(head.face_up)
    run(head.face_middle)
    run(head.face_left)
    run(head.face_level)

    run(head.face_ahead)
