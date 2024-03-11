#!/usr/bin/python3

from utils import sleep_ms
from cmd_proxy import CmdProxy

class Head:
    def __init__(self, proxy):
        self.proxy = proxy
        print(f'Initialised Head')

    def set_x_position(self, position):
        self.proxy.set_head_rotation(position)

    def set_y_position(self, position):
        self.proxy.set_head_left(position)
        self.proxy.set_head_right(position)

    def face_ahead(self):
        print(f'Face ahead')
        self.face_middle()
        self.face_level()

    def face_left(self):
        print(f'Face left')
        self.proxy.set_head_rotation(2000)

    def face_middle(self):
        print(f'Face middle')
        self.proxy.set_head_rotation(1000)

    def face_right(self):
        print(f'Face right')
        self.proxy.set_head_rotation(0)

    def face_up(self):
        print(f'Face up')
        self.proxy.set_head_left(2000)
        self.proxy.set_head_right(2000)

    def face_level(self):
        print(f'Face level')
        self.proxy.set_head_left(1000)
        self.proxy.set_head_right(1000)

    def face_down(self):
        print(f'Face down')
        self.proxy.set_head_left(0)
        self.proxy.set_head_right(0)

    def tilt_left(self):
        print(f'Tilt left')
        self.proxy.set_head_left(0)
        self.proxy.set_head_right(2000)

    def tilt_right(self):
        print(f'Tilt right')
        self.proxy.set_head_left(2000)
        self.proxy.set_head_right(0)


if __name__ == '__main__':
    proxy = CmdProxy()
    head = Head(proxy)

    def run(action):
        action()
        sleep_ms(2000)

    # actions
    run(head.tilt_left)
    run(head.face_ahead)
    run(head.tilt_right)
    run(head.face_ahead)

    run(head.face_left)
    run(head.face_ahead)
    run(head.face_right)
    run(head.face_ahead)

    run(head.face_up)
    run(head.face_down)


    run(head.face_ahead)
