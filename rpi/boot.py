#!/usr/bin/python3

from sound import Sound
from robot import Robot

def main():
    sound = Sound()
    sound.hello()
    Robot().run()


if __name__ == '__main__':
    main()
