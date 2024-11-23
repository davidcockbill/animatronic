#!/usr/bin/python3

from led_panel import LedPanel
from sound import Sound
from cmd_proxy import CmdProxy
from head import Head
from eyes import Eyes
from imutils.video import VideoStream


class Context:
    def __init__(self):
        self.led_panel = LedPanel()
        self.sound = Sound()
        self.proxy = CmdProxy()
        self.head = Head(self.proxy)
        self.eyes = Eyes(self.proxy)
        self.capture = VideoStream(usePiCamera=True).start()
