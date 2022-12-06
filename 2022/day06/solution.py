from collections import deque
from typing import Deque, Iterable

class Device():
    buffer: Deque
    position: int
    signal: str
    unique_chars: int

    def __init__(self, signal: str, unique_chars: int):
        self.buffer = deque()
        self.signal = signal
        self.unique_chars = unique_chars
        for c in self.signal[:self.unique_chars]:
            self.buffer.append(c)
        self.position = self.unique_chars - 1

    def find_start(self):
        """Finds the start position in the signal"""
        while not self.at_start():
            self.position += 1
            self.input_char(self.signal[self.position])

        self.position += 1
        return self.position

    def input_char(self, char: str):
        """Add a char to the buffer"""
        assert len(self.buffer) == self.unique_chars
        self.buffer.append(char)
        self.buffer.popleft()

    def at_start(self) -> bool:
        """Have we reached the start of the signal?"""
        return True if len(set(self.buffer)) == self.unique_chars else False


def pt1(stream: str):
    """part 1"""
    d = Device(signal=stream, unique_chars=4)
    start = d.find_start()
    d.buffer.clear()
    return start


def pt2(stream: str):
    """part 2"""
    d = Device(signal=stream, unique_chars=14)
    start = d.find_start()
    d.buffer.clear()
    return start