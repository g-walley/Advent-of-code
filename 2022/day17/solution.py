from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set
from collections import deque


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
        self.right = max([part.x for part in self.parts])

    def move(self, direction: Point2D) -> List[Point2D]:
        new_parts = []
        for part in self.parts:
            new_parts.append(part + direction)
        return new_parts

    def blow(self, direction: str) -> List[Point2D]:
        assert direction == "<" or direction == ">", "Direction Invalid!"
        return self.move(
            direction=Point2D(-1, 0) if direction == "<" else Point2D(1, 0)
        )

    def drop(self) -> List[Point2D]:
        return self.move(direction=Point2D(0, -1))

    @property
    def parts_sorted_bottom_up(self):
        return sorted(self.parts, key=lambda x: x.y)


def rock_shape_generator():
    d = deque(shapes)
    while True:
        d.append(next := d.popleft())
        yield next

def wind_generator(raw_input: Path) -> str:
    d = deque(list(raw_input.read_text(encoding='utf-8')))
    while True:
        d.append(next := d.popleft())
        yield next


def collision(rock_positions: List[Point2D], world: Set[Point2D]) -> bool:
    return True if set(rock_positions).intersection(world) else False


def print_world(static_points, rock: Rock):
    world = "\t|-------|\n\n"
    all_y = [p.y for p in static_points]
    all_y.extend([r_p.y for r_p in rock.parts])
    max_y = max(all_y)
    for y in range(0, max_y + 1):
        row = ""
        for x in range(LEFT_LIMIT, RIGHT_LIMIT + 1):
            if (p := Point2D(x, y)) in static_points:
                row += "#"
            elif p in rock.parts:
                row += "@"
            else:
                row += "."
        world = f"{y}\t|{row}|\n{world}"
    print(world)


def pt1(raw_input: Path):
    """part 1"""
    rock_gen = rock_shape_generator()
    wind_gen = wind_generator(raw_input)

    static_points: Set[Point2D] = set()

    top = -1
    for i in range(2022):
        r = Rock(shape=next(rock_gen), bottom_row=top + 4)
        # print("New Rock")
        # print_world(static_points, r)

        falling = True
        while falling:
            new_r_position = r.blow(d:= next(wind_gen))
            # print(f"Wind: {d}")
            out_of_bounds = any([part.x < LEFT_LIMIT or RIGHT_LIMIT < part.x for part in new_r_position])
            if not out_of_bounds:
                if not collision(new_r_position, static_points):
                    r.parts = new_r_position

            # print_world(static_points, r)

            new_r_position = r.drop()
            # print("Drop 1")
            out_of_bounds = any([part.y < 0 for part in new_r_position])
            if out_of_bounds or collision(new_r_position, static_points):
                for point in r.parts:
                    static_points.add(point)

                falling = False
            else:
                r.parts = new_r_position

            # print_world(static_points, r)

        y_to_cmp = [top]
        y_to_cmp.extend([part.y for part in r.parts])
        top = max(y_to_cmp)
        print(f"Top: {top}")

    return(top + 1)


def pt2(raw_input):
    """part 2"""
    start_wind = deque(list(raw_input.read_text(encoding='utf-8')))
    winds = deepcopy(start_wind)

    start_rocks = deque(shapes)
    rocks = deepcopy(start_rocks)

    static_points: Set[Point2D] = set()

    top = -1
    for i in range(1000000000000):

        if winds == start_wind and rocks == start_rocks and i != 0:
            print_world(start_rocks)

        shape = rocks.popleft()
        rocks.append(shape)

        r = Rock(shape=shape, bottom_row=top + 4)
        # print("New Rock")
        # print_world(static_points, r)

        falling = True
        while falling:
            wind_dir = winds.popleft()
            winds.append(wind_dir)
            new_r_position = r.blow(wind_dir)
            # print(f"Wind: {wind_dir}")
            out_of_bounds = any([part.x < LEFT_LIMIT or RIGHT_LIMIT < part.x for part in new_r_position])
            if not out_of_bounds:
                if not collision(new_r_position, static_points):
                    r.parts = new_r_position

            # print_world(static_points, r)

            new_r_position = r.drop()
            # print("Drop 1")
            out_of_bounds = any([part.y < 0 for part in new_r_position])
            if out_of_bounds or collision(new_r_position, static_points):
                for point in r.parts:
                    static_points.add(point)

                falling = False
            else:
                r.parts = new_r_position

            # print_world(static_points, r)

        y_to_cmp = [top]
        y_to_cmp.extend([part.y for part in r.parts])
        top = max(y_to_cmp)
        if i % 100000 == 0:
            print(f"Shape {i} | Top: {top}")

    return(top + 1)
