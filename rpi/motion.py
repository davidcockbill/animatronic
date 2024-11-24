#!/usr/bin/python3

import cv2
import numpy as np
from imutils.video import VideoStream
from utils import sleep_ms, get_cpu_temperature


class MotionDetector:
    def __init__(self, capture):
        self.capture = capture
        self.last_mean = 0
        sleep_ms(500)

    def check_motion(self):
        frame = self.capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        mean = np.mean(gray)
        motion = np.abs(mean - self.last_mean) > 0.6
        self.last_mean = mean
        return motion


if __name__ == '__main__':
    capture = VideoStream(usePiCamera=True).start()
    detector = MotionDetector(capture)

    print('Running ...')
    count = 0
    while True:
        motion = detector.check_motion()
        if motion:
            cpu_temperature = get_cpu_temperature()
            print(f'[{count}] Motion detected: {cpu_temperature:.1f}C')
            count += 1
        
        sleep_ms(100)