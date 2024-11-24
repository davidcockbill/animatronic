#!/usr/bin/python3

from utils import ms_timestamp
from random import randrange, choices

from context import Context
from motion import MotionDetector

class Actions:
    def __init__(self, context, actions, random=True):
        self.context = context
        self.blink_timestamp = Actions._blink_timestamp()
        self.actions = actions
        self.random_action = random
        self.action_idx = 0
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
            self.context.eyes.blink()
            self.blink_timestamp = Actions._blink_timestamp()

    def _get_action(self):
        if self.random_action:
            return self._get_random_action()
        return self._get_sequential_action()

    def _get_random_action(self):
        population = self.actions
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        return choices(population, weights, k=1)[0](self.context)
    
    def _get_sequential_action(self):
        action = self.actions[self.action_idx]
        self.action_idx += 1
        self.action_idx %= len(self.actions)
        return action(self.context)


class DefaultActions(Actions):
    def __init__(self, context):
        actions = [
            LookLeft,
            LookRight,
            LookUp,
            LookDown,
            Sleep,
            Shifty,
            Tilt,
            LookUp,
            CrossEyed,
        ]
        super().__init__(context, actions, random=True)


class SleeperActions(Actions):
    def __init__(self, context):
        actions = [
            Sleep,
            Tilt,
            Shifty,
        ]
        super().__init__(context, actions, random=False)


class Action:
    def __init__(self, name, context, steps, blink=True):
        self.name = name
        self.head = context.head
        self.eyes = context.eyes
        self.sound = context.sound
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
        self.step_idx = 0
        return True


class LookLeft(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        steps=[
            ([head.face_left, eyes.look_left], 1000),
            ([head.face_ahead, eyes.look_ahead], 200), 
        ]
        super().__init__('Look Left', context, steps)


class LookRight(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        steps=[
            ([head.face_right, eyes.look_right], 1000),
            ([head.face_ahead, eyes.look_ahead], 200),
        ]
        super().__init__('Look Right', context, steps)


class LookUp(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        steps=[
            ([head.face_up, eyes.look_up, eyes.full_open_eyes], 1000),
            ([head.face_level, eyes.look_ahead, eyes.open_eyes], 200), 
        ]
        super().__init__('Look Up', context, steps)


class LookDown(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        steps=[
            ([head.face_down, eyes.look_down], 1000),
            ([head.face_level, eyes.look_ahead, eyes.open_eyes], 200),
        ]
        super().__init__('Look Down', context, steps)


class Tilt(Action):
    def __init__(self, context): 
        head = context.head
        eyes = context.eyes
        steps=[
            ([self.tilt], 600),
        ]
        super().__init__('Tilt', context, steps)

    def tilt(self):
        population=[
            self.head.tilt_left,
            self.head.tilt_right,
            ]
        
        weight = 1.0 / len(population)
        weights = [weight for i in range(len(population))]
        choices(population, weights, k=1)[0]()


class Sleep(Action):
    def __init__(self, context):
        self.context = context
        self.detector = MotionDetector(context.capture)
        super().__init__('Sleep', context, [], blink=False)
        self._sleep()
        print('Sleeping...')
    
    def pulse(self):
        done = False
        current_ms = ms_timestamp()
        if current_ms > self.next_ms:
            motion = self.detector.check_motion()
            if motion:
                self._awake()
                done = True
        else:
            self.detector.check_motion()
        return done

    def _sleep(self):
        self.context.head.face_down()
        self.context.eyes.close_eyes()
        self.next_ms = self._get_next_ms(2000)

    def _awake(self):
        print('Waking up...')
        self.context.eyes.open_eyes()
        self.context.head.face_ahead()
        self.sound.hello()


class CrossEyed(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        sound = context.sound
        steps=[
            ([head.face_ahead, eyes.cross_eyed], 100),
            ([sound.raspberry], 1000),
            ([head.face_ahead, eyes.look_ahead], 200),
        ]
        super().__init__('Cross Eyed', context, steps, blink=False)


class Shifty(Action):
    def __init__(self, context):
        head = context.head
        eyes = context.eyes
        steps=[
            ([head.face_level], 500),
            ([eyes.look_left], 200),
            ([eyes.look_right], 200),
            ([eyes.look_ahead], 500), 
        ]
        super().__init__('Shifty', context, steps)


if __name__ == '__main__':
    context = Context()
    actions = SleeperActions(context)
    while True:
        actions.pulse()
