#!/usr/bin/python3

from utils import ms_timestamp
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
            Tilt(self.head, self.eyes, self.sound),
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
        self.step_idx = 0
        self.steps = steps
        self.blink = blink
        self.next_ms = self._get_next_ms(0)

    def pulse(self):
        done = False
        current_ms = ms_timestamp()
        if current_ms > self.next_ms:
            done = self._action()
        return done

    def should_blink(self):
        return self.blink
    
    @staticmethod
    def _get_next_ms(await_time):
        return ms_timestamp() + await_time

    def _action(self):
        if self.step_idx < len(self.steps):
            print(f'{self.name}: step {self.step_idx}')
            actions, await_time = self.steps[self.step_idx]
            [action() for action in actions]
            self.step_idx += 1
            self.next_ms = self._get_next_ms(await_time)
            return False
        return True


class LookLeft(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([head.face_left, eyes.look_left], 1000),
            ([head.face_ahead, eyes.look_ahead], 200), 
        ]
        super().__init__('Look Left', head, eyes, sound, steps)


class LookRight(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([head.face_right, eyes.look_right], 1000),
            ([head.face_ahead, eyes.look_ahead], 200),
        ]
        super().__init__('Look Right', head, eyes, sound, steps)


class LookUp(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([head.face_up, eyes.look_up, eyes.full_open_eyes], 1000),
            ([head.face_level, eyes.look_ahead, eyes.open_eyes], 200), 
        ]
        super().__init__('Look Up', head, eyes, sound, steps)


class LookDown(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([head.face_down, eyes.look_down], 1000),
            ([head.face_level, eyes.look_ahead, eyes.open_eyes], 200),
        ]
        super().__init__('Look Down', head, eyes, sound, steps)


class Tilt(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([self.tilt], 600),
        ]
        super().__init__('Tilt', head, eyes, sound, steps)

    def tilt(self):
        population=[
            self.head.tilt_left,
            self.head.tilt_right,
            ]
        
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        choices(population, weights, k=1)[0]()


class Sleep(Action):
    def __init__(self, head, eyes, sound, blink=False):
        steps=[
            ([head.face_down, eyes.close_eyes], 5000), 
            ([head.face_ahead, eyes.open_eyes], 100),
            ([sound.hello], 10),
        ]
        super().__init__('Sleep', head, eyes, sound, steps)


class CrossEyed(Action):
    def __init__(self, head, eyes, sound, blink=False):
        steps=[
            ([head.face_ahead, eyes.cross_eyed], 100),
            ([sound.raspberry], 1000),
            ([head.face_ahead, eyes.look_ahead], 200),
        ]
        super().__init__('Cross Eyed', head, eyes, sound, steps)


class Shifty(Action):
    def __init__(self, head, eyes, sound):
        steps=[
            ([head.face_level], 500),
            ([eyes.look_left], 200),
            ([eyes.look_right], 200),
            ([eyes.look_ahead], 500), 
        ]
        super().__init__('Shifty', head, eyes, sound, steps)


if __name__ == '__main__':
    sound = Sound()
    proxy = CmdProxy()
    head = Head(proxy)
    eyes = Eyes(proxy)
    actions = Actions(head, eyes, sound)
    while True:
        actions.pulse()