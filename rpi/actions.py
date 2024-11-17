#!/usr/bin/python3

from utils import sleep_ms, ms_timestamp
from random import randrange, choices

from sound import Sound
from cmd_proxy import CmdProxy
from head import Head
from eyes import Eyes

class Actions:
    def __init__(self, head, eyes, sound):
        self.head = head
        self.eyes = eyes
        self.sound = sound
        self.blink_timestamp = Actions._blink_timestamp()
        self.reset()

    def reset(self):
        self.action = self._get_action()

    def pulse(self):
        if self.action.should_blink():
            self._blink()
        done = self.action.pulse()
        if done:
            self.action = self._get_action()

    def shutdown(self):
        self.head.reset()
        self.eyes.reset()

    @staticmethod
    def _blink_timestamp():
        return ms_timestamp() + randrange(1000, 8000)

    def _blink(self):
        if ms_timestamp() > self.blink_timestamp:
            self.eyes.blink()
            self.blink_timestamp = Actions._blink_timestamp()

    def _get_action(self):
        population=[
            LookLeft(self.head, self.eyes, self.sound),
            LookRight(self.head, self.eyes, self.sound),
            LookUp(self.head, self.eyes, self.sound),
            LookDown(self.head, self.eyes, self.sound),
            Sleep(self.head, self.eyes, self.sound),
            Shifty(self.head, self.eyes, self.sound),
            Awake(self.head, self.eyes, self.sound),
            LookUp(self.head, self.eyes, self.sound),
            CrossEyed(self.head, self.eyes, self.sound),
        ]
        
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        return choices(population, weights, k=1)[0]


class Action:
    def __init__(self, name, head, eyes, sound, steps, blink=True):
        self.name = name
        self.head = head
        self.eyes = eyes
        self.sound = sound
        self.action_idx = 0
        self.steps = steps
        self.blink = blink
        self.next_ms = self._get_next_ms()

    def pulse(self):
        done = False
        current_ms = ms_timestamp()
        if current_ms > self.next_ms:
            done = self._action()
            self.next_ms = self._get_next_ms()
        return done

    def should_blink(self):
        return self.blink
    
    def wait(self):
        sleep_ms(100)
    
    @staticmethod
    def _get_next_ms():
        return ms_timestamp() + 250

    def _action(self):
        if self.action_idx < len(self.steps):
            print(f'{self.name}: action {self.action_idx}')
            [action() for action in self.steps[self.action_idx]]
            self.action_idx += 1
            return False
        return True


class LookLeft(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [head.face_left, eyes.look_left],
            [self.wait], 
            [head.face_ahead, eyes.look_ahead], 
        ]
        super().__init__('Look Left', head, eyes, sound, steps)


class LookRight(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [head.face_right, eyes.look_right], 
            [self.wait], 
            [head.face_ahead, eyes.look_ahead], 
        ]
        super().__init__('Look Right', head, eyes, sound, steps)


class LookUp(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [head.face_up, eyes.look_up, eyes.full_open_eyes],
            [self.wait], 
            [head.face_level, eyes.look_ahead, eyes.open_eyes], 
        ]
        super().__init__('Look Up', head, eyes, sound, steps)

class LookDown(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [head.face_down, eyes.look_down],
            [self.wait], 
            [head.face_level, eyes.look_ahead, eyes.open_eyes], 
        ]
        super().__init__('Look Up', head, eyes, sound, steps)


class Awake(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [self.tilt],
            [self.awake],
            [head.face_level],
        ]
        super().__init__('Awake', head, eyes, sound, steps)

    def tilt(self):
        population=[
            self.head.tilt_left,
            self.head.tilt_right,
            self.head.face_level,
            ]
        
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        choices(population, weights, k=1)[0]()

    def awake(self):
        for blinks in range(randrange(1, 5)):
            sleep_ms(randrange(500,5000))
            self.eyes.blink()


class Sleep(Action):
    def __init__(self, head, eyes, sound, blink=False):
        steps=[
            [head.face_down, eyes.close_eyes], 
            [self.wait], 
            [head.face_ahead, eyes.open_eyes], 
        ]
        super().__init__('Sleep', head, eyes, sound, steps)

    def wait(self):
        sleep_ms(5000)


class CrossEyed(Action):
    def __init__(self, head, eyes, sound, blink=False):
        steps=[
            [head.face_ahead, eyes.cross_eyed],
            [sound.raspberry],
            [self.wait], 
            [head.face_ahead, eyes.look_ahead], 
        ]
        super().__init__('Cross Eyed', head, eyes, sound, steps)

    def wait(self):
        sleep_ms(500)


class Shifty(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            [head.face_level], 
            [self.wait], 
            [eyes.look_left], 
            [self.wait], 
            [eyes.look_right], 
            [self.wait], 
            [eyes.look_ahead], 
        ]
        super().__init__('Shifty', head, eyes, sound, steps)

    def wait(self):
        sleep_ms(100)


if __name__ == '__main__':
    sound = Sound()
    proxy = CmdProxy()
    head = Head(proxy)
    eyes = Eyes(proxy)
    actions = Actions(head, eyes, sound)
    while True:
        actions.pulse()