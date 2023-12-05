from __future__ import annotations
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import re
from string import digits, punctuation
from typing import Dict, Optional, Set


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def is_adjacent(self, other):
        return (
            ((self.x - 1) <= other.x)
            and (other.x <= (self.x + 1))
            and ((self.y - 1) <= other.y)
            and (other.y <= (self.y + 1))
        )

    @property
    def adjacent(self):
        return {
            Point2D(self.x - 1, self.y - 1),
            Point2D(self.x - 1, self.y),
            Point2D(self.x - 1, self.y + 1),
            Point2D(self.x + 1, self.y - 1),
            Point2D(self.x + 1, self.y),
            Point2D(self.x + 1, self.y + 1),
            Point2D(self.x, self.y + 1),
            Point2D(self.x, self.y - 1),
        }

    @property
    def left(self):
        return Point2D(self.x - 1, self.y)

    @property
    def right(self):
        return Point2D(self.x + 1, self.y)

@dataclass
class Number:
    raw: str
    points: Set

    @property
    def value(self) -> int:
        return int(self.raw)

class Board:
    all: dict[Point2D, str]
    filt = digits
    def __init__(self, rows: list[str], filt: Optional[str]):
        if filt:
            self.filt += filt
        self.all = {
            Point2D(x, y): char
            for x, row in enumerate(rows)
            for y, char in enumerate(row)
            if char in self.filt
        }

    def numbers(self):
        numbers = []
        to_consider = deque(list(self.all.keys()))
        previous = None
        while to_consider:
            c = to_consider.popleft()
            if previous and c.left==:






        return numbers




class Pt1Board(Board):
    def __init__(self, rows: list[str], filt=None):
        super().__init__(rows=rows, filt=None)

class Pt2Board(Board):
    def __init__(self, rows: list[str], filt=None):
        super().__init__(rows=rows, filt="*")

def pt1(raw_input: Path):
    """part 1"""
    # Get length of lines:
    lines = raw_input.read_text().splitlines()
    shape = (len(lines[0]), len(lines))
    board = Pt1Board(rows=lines)

    numbers = board.numbers()
    total = 0
    for line_idx, line in enumerate(lines):
        matches = re.finditer(r"\d+", line)
        for match in matches:
            span = match.span()
            h_min = 0 if (span[0] == 0) else span[0] - 1
            h_max = shape[0] if (span[1] == shape[0]) else span[1] + 1
            v_min = 0 if (line_idx == 0) else line_idx - 1
            v_max = shape[1] if (line_idx == shape[1]) else line_idx + 1

            relevant_lines = lines[v_min : v_max + 1]

            section = "".join([line[h_min:h_max] for line in relevant_lines])
            remove_digits = str.maketrans("", "", digits)
            remove_full_stops = str.maketrans("", "", ".")
            result = section.translate(remove_digits)
            result = result.translate(remove_full_stops)
            if result:
                total += int(match.group())
    return total


def pt2(raw_input: Path):
    """part 2"""
    lines = raw_input.read_text().splitlines()

    for star in board.stars:
        adj_numbers = {
            point: board.relevant[point] for point in star.adjacent.intersection(board.numbers)
        }
    # First find location of the "*", and store as tuple pairs in a set
    stars = {
        Point2D(line_idx, match.span()[0])
        for line_idx, line in enumerate(lines)
        for match in re.finditer(r"\*", line)
    }

    # Find location of all numbers Map numbers as x, x+1, x+n == num
    nums = {
        Point2D(line_idx, i): int(match.group())
        for line_idx, line in enumerate(lines)
        for match in re.finditer(r"\d+", line)
        for i in range(match.span()[0], match.span()[1])
    }

    # For each star, find numbers adjacent to it.
    gears: Dict[Point2D, set[int]] = defaultdict(set)
    for gear in stars:
        for num_pos, num_value in nums.items():
            if gear.is_adjacent(num_pos):
                gears[gear].add(num_value)
                if len(gears[gear]) >= 2:
                    break

    return sum(
        list(nums)[0] * list(nums)[1] for nums in gears.values() if len(nums) == 2
    )
