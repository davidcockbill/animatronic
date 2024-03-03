#!/usr/bin/python3

import spidev


class CmdProxy:
    PROTOCOL_START = 0x55
    PROTOCOL_END = 0xAA
    
    LEFT_EYE_X_CMD = 0
    LEFT_EYE_Y_CMD = 1
    RIGHT_EYE_X_CMD = 2
    RIGHT_EYE_Y_CMD = 3
    EYE_LIDS_CMD = 4
    HEAD_ROTATION_CMD = 5
    HEAD_RIGHT_CMD = 6
    HEAD_LEFT_CMD = 7

    def __init__(self):
        spi_bus = 0
        spi_device = 0
        spi = spidev.SpiDev()
        spi.open(spi_bus, spi_device)
        spi.max_speed_hz = 1000000
        spi.mode = 0

        self.spi = spi
        print('Started SPI')

    def shutdown(self):
        self.spi.close()

    def set_left_eye_x(self, position):
        self._send(CmdProxy.LEFT_EYE_X_CMD, position)

    def set_left_eye_y(self, position):
        self._send(CmdProxy.LEFT_EYE_Y_CMD, position)

    def set_right_eye_x(self, position):
        self._send(CmdProxy.RIGHT_EYE_X_CMD, position)

    def set_right_eye_y(self, position):
        self._send(CmdProxy.RIGHT_EYE_Y_CMD, position)

    def set_eye_lids(self, position):
        self._send(CmdProxy.EYE_LIDS_CMD, position)

    def set_head_rotation(self, position):
        self._send(CmdProxy.HEAD_ROTATION_CMD, position)

    def set_head_right(self, position):
        self._send(CmdProxy.HEAD_RIGHT_CMD, position)

    def set_head_left(self, position):
        self._send(CmdProxy.HEAD_LEFT_CMD, position)

    def _send(self, key, value):
        data = []
        data.append(CmdProxy.PROTOCOL_START)
        data.append(key)
        data.append(value >> 8 & 0x00FF)
        data.append(value & 0x00FF)
        data.append(CmdProxy.PROTOCOL_END)
        self.spi.xfer2(data)


def main():
    proxy = CmdProxy()
    proxy.set_left_eye_x(1000)
    proxy.set_left_eye_y(1000)

    proxy.set_right_eye_x(1000)
    proxy.set_right_eye_y(1000)

    proxy.set_eye_lids(2000)

    proxy.set_head_rotation(1000)
    proxy.set_head_left(1000)
    proxy.set_head_right(900)
    proxy.shutdown()


if __name__ == '__main__':
    main()