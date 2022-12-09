from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Vector2D:
    x: int
    y: int

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)


@dataclass
class Head(Vector2D):



@dataclass
class Tail(Vector2D):
    ...

directions = {
    "R": Vector2D(1,  0);
    "L": Vector2D(-1, 0);
    "U": Vector2D(0,  1);
    "D": Vector2D(0, -1);
}

def pt1(path: Path):
    """part 1"""

    head = Head(0, 0)
    tail = Tail(0, 0)


def pt2(raw_input):
    """part 2"""