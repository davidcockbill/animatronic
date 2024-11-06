#!/usr/bin/python3

from cmd_proxy import CmdProxy
from utils import sleep_ms


class Eyes:
    def __init__(self, proxy):
        self.proxy = proxy
        print(f'Initialised Eyes')

    def set_x_position(self, position):
        self.proxy.set_left_eye_x(position)
        self.proxy.set_right_eye_x(position)

    def set_y_position(self, position):
        self.proxy.set_left_eye_y(position)
        self.proxy.set_right_eye_y(position)

    def set_lids_position(self, position):
       self.proxy. set_eye_lids(position)

    def default_eyes(self):
        print(f'Defaulting ...')
        self.look_ahead()
        self.open_eyes()
        print(f'Defaulted')

    def look_ahead(self):
        print(f'Look ahead')
        self.proxy.set_left_eye_x(1000)
        self.proxy.set_left_eye_y(1000)
        self.proxy.set_right_eye_x(1000)
        self.proxy.set_right_eye_y(1000)

    def look_left(self):
        print(f'Look left')
        self.proxy.set_left_eye_x(2000)
        self.proxy.set_right_eye_x(2000)

    def look_right(self):
        print(f'Look right')
        self.proxy.set_left_eye_x(0)
        self.proxy.set_right_eye_x(0)

    def cross_eyed(self):
        print(f'Cross eyed')
        self.proxy.set_left_eye_x(0)
        self.proxy.set_right_eye_x(2000)

    def look_up(self):
        print(f'Look up')
        self.proxy.set_left_eye_y(2000)
        self.proxy.set_right_eye_y(2000)

    def look_down(self):
        print(f'Look down')
        self.proxy.set_left_eye_y(0)
        self.proxy.set_right_eye_y(0)

    def close_eyes(self):
        self.proxy.set_eye_lids(0)

    def wide_eyes(self):
        self.proxy.set_eye_lids(1500)

    def open_eyes(self):
        self.proxy.set_eye_lids(1000)

    def full_open_eyes(self):
        self.proxy.set_eye_lids(2000)

    def blink(self):
        self.close_eyes()
        sleep_ms(100)
        self.open_eyes()


if __name__ == '__main__':
    proxy = CmdProxy()
    eyes = Eyes(proxy)

    def run(action):
        action()
        sleep_ms(1000)

    # actions
    run(eyes.look_ahead)
    run(eyes.cross_eyed)
    run(eyes.blink)
    run(eyes.look_right)
    run(eyes.look_ahead)
    run(eyes.blink)
    run(eyes.look_left)
    run(eyes.look_ahead)
    run(eyes.blink)
    run(eyes.look_up)
    run(eyes.look_down)

    run(eyes.look_ahead)
