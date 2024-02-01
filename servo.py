#!/usr/bin/python3

from overrides import override

SLOW_STEPS = 0.002
FAST_STEPS = 0.006

class Servo:
    def __init__(self, kit, servo_idx, midpoint_fraction, max_midpoint_offset, servo_reversed=False):
        self.kit = kit
        self.servo_idx = servo_idx
        self.min_fraction = midpoint_fraction - max_midpoint_offset
        self.mid_fraction = midpoint_fraction
        self.max_fraction = midpoint_fraction + max_midpoint_offset
        self.reversed = servo_reversed
        self.reset()

    def reset(self):
        self.centre()

    def centre(self):
        self._set_fraction(self.mid_fraction)

    def position(self, position):
        midpoint_offset = position / 2
        fraction = self.mid_fraction - midpoint_offset if self.reversed else self.mid_fraction + midpoint_offset
        self._set_fraction(fraction)

    def set_pulse_width_range(self, min_pulse, max_pulse):
        self.kit.servo[self.servo_idx].set_pulse_width_range(min_pulse, max_pulse)

    def actuation_range(self, actuation_range):
        self.kit.servo[self.servo_idx].actuation_range = actuation_range
    
    def _set_fraction(self, fraction):
        fraction = self._constrain_fraction(fraction)
        self.kit.servo[self.servo_idx].fraction = float(fraction)

    def _constrain_fraction(self, fraction):
        constrained = max(fraction, self.min_fraction)
        constrained = min(constrained, self.max_fraction)
        return constrained

    def __str__(self):
        return f'idx={self.servo_idx}, min={self.min_fraction:.2f}, mid={self.mid_fraction:.2f}, max={self.max_fraction:.2f}, reversed={self.reversed}'
    

class Smoothed_Servo(Servo):
    def __init__(self, kit, servo_idx, servo_midpoint, servo_range, servo_reversed=False):
        super().__init__(kit, servo_idx, servo_midpoint, servo_range, servo_reversed)
        self.desired_position = 0
        self.current_position = 0
        self.done_diff = 0.01
        self.linear_movement = True
        self.linear_movement_step = FAST_STEPS
        print(f'[{self.servo_idx}] initialised')

    def pulse(self):
        done = True
        # print(f'[{self.servo_idx}] desired={self.desired_position}, diff={abs(self.desired_position - self.current_position)}')

        if abs(self.desired_position - self.current_position) > self.done_diff:
            # Moving
            super().position(self._get_new_position())
            done = False
        elif self.current_position != self.desired_position:
            # Finished
            super().position(self.desired_position)
            self.current_position = self.desired_position
            done = True
        return done

    def slow(self):
        pass#self.linear_movement_step = SLOW_STEPS

    def fast(self):
        self.linear_movement_step = FAST_STEPS

    @override
    def centre(self):
        self.desired_position = 0

    @override
    def position(self, position):
        self.desired_position = position

    def _get_new_position(self):
        new_position = self._linear_new_position() if self.linear_movement else self._proportional_new_position()
        self.current_position = new_position
        return new_position

    def _linear_new_position(self):
        if self.current_position < self.desired_position:
            return self.current_position + self.linear_movement_step
        elif self.current_position > self.desired_position:
            return self.current_position - self.linear_movement_step
        return self.desired_position

    def _proportional_new_position(self):
        return (self.desired_position * 0.01) + (self.current_position * 0.99)



