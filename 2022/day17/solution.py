from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set


shapes = [
    ["@@@@"],
    [".@.", "@@@", ".@."],
    ["@@@", "..@", "..@"],
    4 * ["@"],
    2 * ["@@"],
]

LEFT_LIMIT = 0
RIGHT_LIMIT = 6


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D):
        return Point2D(self.x - other.x, self.y - other.y)


@dataclass()
class Rock:
    parts: List[Point2D]
    stationary: bool = False

    def __init__(self, shape: List[str], bottom_row: int):
        self.parts = []
        for row_idx, row in enumerate(shape):
            for elem_idx, elem in enumerate(row):
                if elem != "@":
                    continue
                x = 2 + elem_idx
                y = bottom_row + row_idx
                self.parts.append(Point2D(x, y))

        self.parts = sorted(self.parts, key=lambda x: x.x)

        self.left = 2
        self.right = x

    def blow(self, direction: str):
        if not self.stationary:
            if direction == "<":
                if self.left > 0:
                    ...
                    self.left -= 1
            elif direction == ">":
                if self.right < 6:
                    ...
                    self.right += 1
            else:
                assert False, "Direction Invalid!"

    @property
    def parts_sorted_bottom_up(self):
        return sorted(self.parts, key=lambda x: x.y)

    # def __add__(self, other: Point2D):
    #     return Point2D(self.x + other.x, self.y + other.y)

    # def __sub__(self, other: Point2D):
    #     return Point2D(self.x - other.x, self.y - other.y)


def pt1(raw_input: Path):
    """part 1"""
    print("\n\n")
    print(shapes)

    r = Rock(shape=shapes[1], bottom_row=2)
    print(r.parts_sorted_bottom_up)
    print("\n\n")


def pt2(raw_input):
    """part 2"""
