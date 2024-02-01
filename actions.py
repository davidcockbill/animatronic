#!/usr/bin/python3

from utils import sleep_ms, ms_timestamp
from random import randrange, choices


class Actions:
    def __init__(self, head, eyes):
        self.head = head
        self.eyes = eyes
        self.blink_timestamp = Actions._blink_timestamp()
        self.action = self._get_action()

    def pulse(self):
        if self.action.should_blink():
            self._blink()
        done = self.action.pulse()
        if done:
            self.action = self._get_action()
        Actions._pulse_delay()

    def shutdown(self):
        self.head.reset()
        self.eyes.reset()
        done = False
        while not done:
            eyes_done = self.eyes.pulse()
            head_done = self.head.pulse()
            done = eyes_done and head_done

    @staticmethod
    def _blink_timestamp():
        return ms_timestamp() + randrange(1000, 8000)

    def _blink(self):
        if ms_timestamp() > self.blink_timestamp:
            self.eyes.blink()
            self.blink_timestamp = Actions._blink_timestamp()

    @staticmethod
    def _pulse_delay():
        sleep_ms(0.00001)

    def _get_action(self):
        population=[
            LookLeft(self.head, self.eyes),
            LookRight(self.head, self.eyes),
            Sleep(self.head, self.eyes),
            Shifty(self.head, self.eyes),
            Awake(self.head, self.eyes),
            LookUp(self.head, self.eyes),
            CrossEyed(self.head, self.eyes),
            ]
        
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        return choices(population, weights, k=1)[0]


class Action:
    def __init__(self, name, head, eyes, steps, await_ms=0, blink=True):
        self.name = name
        self.head = head
        self.eyes = eyes
        self.action_idx = 0
        self.steps = steps
        self.await_ms = await_ms
        self.blink = blink

    def pulse(self):
        done = False
        eyes_done = self.eyes.pulse()
        head_done = self.head.pulse()
        action_complete = eyes_done and head_done
        if action_complete:
            done = self._action()
        if done:
            sleep_ms(self.await_ms)
        return done

    def should_blink(self):
        return self.blink

    def _action(self):
        if self.action_idx < len(self.steps):
            print(f'{self.name}: action {self.action_idx}')
            [action() for action in self.steps[self.action_idx]]
            self.action_idx += 1
            return False
        return True


class LookLeft(Action):
    def __init__(self, head, eyes):
        steps=[
            [head.face_ahead, eyes.look_ahead], 
            [head.face_left, eyes.look_left], 
            [head.face_ahead, eyes.look_ahead], 
        ]
        super().__init__('Look Left', head, eyes, steps)


class LookRight(Action):
    def __init__(self, head, eyes):
        steps=[
            [head.face_ahead, eyes.look_ahead], 
            [head.face_right, eyes.look_right], 
            [head.face_ahead, eyes.look_ahead], 
        ]
        super().__init__('Look Right', head, eyes, steps)

class LookUp(Action):
    def __init__(self, head, eyes):
        steps=[
            [head.face_level, eyes.look_ahead], 
            [head.face_up, eyes.look_up, eyes.full_open_eyes], 
            [head.face_level, eyes.look_ahead, eyes.open_eyes], 
        ]
        super().__init__('Look Up', head, eyes, steps)

class Awake(Action):
    def __init__(self, head, eyes):
        steps=[
            [self.tilt],
            [self.awake],
            [head.face_level],
        ]
        super().__init__('Awake', head, eyes, steps)

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
    def __init__(self, head, eyes, blink=False):
        steps=[
            [head.slow],
            [head.face_down, eyes.close_eyes], 
            [self.wait], 
            [head.face_ahead, eyes.open_eyes], 
            [head.fast],
        ]
        super().__init__('Sleep', head, eyes, steps)

    def wait(self):
        sleep_ms(5000)

class CrossEyed(Action):
    def __init__(self, head, eyes, blink=False):
        steps=[
            [eyes.slow],
            [head.face_ahead, eyes.cross_eyed], 
            [self.wait], 
            [head.face_ahead, eyes.look_ahead], 
            [eyes.fast],
        ]
        super().__init__('Cross Eyed', head, eyes, steps)

    def wait(self):
        sleep_ms(500)


class Shifty(Action):
    def __init__(self, head, eyes):
        steps=[
            [eyes.slow],
            [head.face_level], 
            [self.wait], 
            [eyes.look_left], 
            [self.wait], 
            [eyes.look_right], 
            [self.wait], 
            [eyes.look_ahead], 
            [eyes.fast], 
        ]
        super().__init__('Shifty', head, eyes, steps)

    def wait(self):
        sleep_ms(100)
