from time import time
from constants import WIDTH
from base import Updatable


class Delay(Updatable):
    """To launch function after a delay"""

    def __init__(self, func, delay=0):
        self.updatables.append(self)
        self.start = time() + delay
        self.to_run = func

    def update(self, dt, t):
        if t >= self.start:
            self.to_run()
            self.updatables.remove(self)
            del self


def map_range(value, in_min, in_max, out_min, out_max):
    """Map a value from a range to another one
    value  : is between in_min and in_max
    result : is the scaled value between out_min and out_max"""
    # length of each range
    in_length = in_max - in_min
    out_length = out_max - out_min
    # Convert in_range into a 0-1 range
    value_scaled = (value - in_min) / in_length

    # Convert the 0-1 range into a value in the out range.
    return out_min + (value_scaled * out_length)


def center_txt(txt):
    return (WIDTH - len(txt) * 4) // 2
