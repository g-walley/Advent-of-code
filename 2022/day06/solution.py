from collections import deque
from typing import Deque

class Device():
    def __init__(self, signal: str, unique_chars: int):
        self.buffer: Deque = deque(signal[:unique_chars], unique_chars)
        self.signal: Deque = deque(signal[unique_chars:])
        self.position: int = unique_chars

    def find_start(self):
        """Finds the start position in the signal"""
        while len(set(self.buffer)) != len(self.buffer):
            self.buffer.append((self.signal.popleft()))
            self.position += 1
        return self.position


def pt1(stream: str):
    return Device(signal=stream, unique_chars=4).find_start()


def pt2(stream: str):
    return Device(signal=stream, unique_chars=14).find_start()