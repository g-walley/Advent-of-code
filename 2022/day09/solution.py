from __future__ import annotations
from collections import deque

from dataclasses import dataclass, field
from pathlib import Path
from typing import Deque, Set
from parse import *


@dataclass(frozen=True)
class Vector2D:
    x: int
    y: int

    def __add__(self, other: Vector2D):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D):
        return Vector2D(self.x - other.x, self.y - other.y)


@dataclass
class Knot:
    tail: Knot | None
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

    def delta_to(self, other: Knot):
        return Vector2D(
            (self.position.x - other.position.x)
            // (abs(self.position.x - other.position.x) or 1),
            (self.position.y - other.position.y)
            // (abs(self.position.y - other.position.y) or 1),
        )

    def move(self, direction: Vector2D):
        self.position += direction
        if self.tail:
            if not self.touching(self.tail):
                self.tail.move(direction=self.delta_to(self.tail))
        else:
            self.visited.add(Vector2D(self.position.x, self.position.y))

    def cells_visited(self) -> int:
        if self.tail:
            return self.tail.cells_visited()
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
        for _ in range(int(input["distance"])):
            instructions.append(direction_vectors[input["direction"]])

    return instructions


def tie_knots_together(number_of_knots: int) -> Knot:
    knots = [Knot(None) for _ in range(number_of_knots)]
    for idx, knot in enumerate(knots):
        knot.tail = knots[idx + 1] if idx < number_of_knots - 1 else None
    return knots[0]


def pt1(path: Path):
    instructions = decode_instructions(path)
    head = tie_knots_together(2)

    while instructions:
        head.move(instructions.popleft())
    return len(head.cells_visited())


def pt2(path: Path):
    """part 2"""
    instructions = decode_instructions(path)
    head = tie_knots_together(10)

    while instructions:
        head.move(instructions.popleft())
    return len(head.cells_visited())
