from __future__ import annotations
from collections import deque

from dataclasses import dataclass, field
from pathlib import Path
from typing import Deque, Set
from parse import *
import sys

gettrace = getattr(sys, "gettrace", None)


@dataclass(frozen=True)
class Vector2D:
    x: int
    y: int

    def __sub__(self, other: Vector2D):
        return Vector2D(self.x - other.x, self.y - other.y)


@dataclass
class Knot:
    child: Knot | None
    position: Vector2D = Vector2D(0, 0)
    visited: Set[Vector2D] = field(default_factory=set)

    def __post_init__(self):
        self.visited.add(self.position)

    def touching(self, other: Knot):
        return (
            max(
                abs(self.position.x - other.position.x),
                abs(self.position.y - other.position.y),
            )
            <= 1
        )

    def delta(self, other: Knot):
        return Vector2D(
            (self.position.x - other.position.x)
            // (abs(self.position.x - other.position.x) or 1),
            (self.position.y - other.position.y)
            // (abs(self.position.y - other.position.y) or 1),
        )

    def move(self, direction: Vector2D):
        self.position = Vector2D(
            self.position.x + direction.x,
            self.position.y + direction.y,
        )
        if self.child:
            if not self.touching(self.child):
                self.child.move(direction=self.delta(self.child))
        else:
            self.visited.add(Vector2D(self.position.x, self.position.y))

    def cells_visited(self) -> int:
        if self.child:
            return self.child.cells_visited()
        return self.visited


direction_vectors = {
    "R": Vector2D(1, 0),
    "L": Vector2D(-1, 0),
    "U": Vector2D(0, 1),
    "D": Vector2D(0, -1),
}


def decode_instructions(file_path: Path) -> Deque[Vector2D]:
    instructions: Deque[Vector2D] = deque()
    for line in file_path.read_text().splitlines():
        input = parse("{direction} {distance}", line.strip()).named
        direction = direction_vectors[input["direction"]]
        distance = int(input["distance"])
        for _ in range(distance):
            instructions.append(direction)

    return instructions


def construct_rope(length):
    head = Knot(child=None)
    current_knot = head
    for _ in range(length - 1):
        current_knot.child = Knot(child=None)
        current_knot = current_knot.child
    return head


def pt1(path: Path):
    """part 1"""

    instructions = decode_instructions(path)
    head = construct_rope(2)
    while instructions:
        instruction = instructions.popleft()
        head.move(instruction)
        if gettrace():
            debug_print(head)

    return len(head.cells_visited())


def debug_print(head: Knot):

    positions = {}
    current_knot = head
    knot_count = 0
    while current_knot:
        if current_knot.position not in positions:
            positions[current_knot.position] = (
                "H" if knot_count == 0 else str(knot_count)
            )
        current_knot = current_knot.child
        knot_count += 1
    if (origin := Vector2D(0, 0)) not in positions:
        positions[origin] = "S"

    for y in range(
        max([pos.y for pos in positions]), min([pos.y for pos in positions]) - 1, -1
    ):
        line_str = ""
        for x in range(
            min([pos.x for pos in positions]), max([pos.x for pos in positions]) + 1
        ):
            char = positions.get(Vector2D(x, y), ".")
            line_str += char

        print(line_str)

    print("\n-----\n")


def pt2(path: Path):
    """part 2"""

    instructions = decode_instructions(path)

    head = construct_rope(10)
    while instructions:
        instruction = instructions.popleft()
        head.move(instruction)
        if gettrace():
            debug_print(head)

    return len(head.cells_visited())
