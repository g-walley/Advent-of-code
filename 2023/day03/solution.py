from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import re
from string import digits, punctuation
from typing import Dict


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


def pt1(raw_input: Path):
    """part 1"""
    # Get length of lines:
    lines = raw_input.read_text().splitlines()
    shape = (len(lines[0]), len(lines))

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
