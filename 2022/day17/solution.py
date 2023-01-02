from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple
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


def get_rock(shape: List[str], bottom_row: int) -> Set[Tuple]:
    return {
        (2 + elem_idx, bottom_row + row_idx)
        for row_idx, row in enumerate(shape)
        for elem_idx, elem in enumerate(row)
        if elem == "@"
    }


def move_right(rock: Set[Tuple]) -> Set[Tuple]:
    return {(x + 1, y) for (x, y) in rock}


def move_left(rock: Set[Tuple]) -> Set[Tuple]:
    return {(x - 1, y) for (x, y) in rock}


def move_down(rock: Set[Tuple]) -> Set[Tuple]:
    return {(x, y - 1) for (x, y) in rock}


def move_up(rock: Set[Tuple]) -> Set[Tuple]:
    return {(x, y + 1) for (x, y) in rock}


def print_world(static_points: Set[Tuple], rock: Set[Tuple]):
    world = "\t|-------|\n\n"
    all_y = [y for (x, y) in static_points]
    all_y.extend([y for (x, y) in rock])
    max_y = max(all_y)
    for y in range(0, max_y + 1):
        row = ""
        for x in range(LEFT_LIMIT, RIGHT_LIMIT + 1):
            if (p := (x, y)) in static_points:
                row += "#"
            elif p in rock:
                row += "@"
            else:
                row += "."
        world = f"{y}\t|{row}|\n{world}"
    print(world)


def create_world_sig(static_objects: Set[Tuple]):
    max_y = max([y for (x, y) in static_objects])
    return frozenset([(x, max_y - y) for (x, y) in static_objects if max_y - y <= 10])


def run(wind: str, max_t: int) -> int:
    seen = {}
    static_objects = set()
    t = 0
    wind_idx = 0
    shape_idx = 0
    max_y = -1
    sig = []
    skipped = 0
    while t < max_t:
        t += 1
        moving = True
        s = shape_idx % len(shapes)
        rock = get_rock(shapes[s], max_y + 4)

        while moving:
            # Drift
            w = wind_idx % len(wind)
            if wind[w] == "<":
                if not any([x == LEFT_LIMIT for (x, y) in rock]):
                    rock = move_left(rock)
                    if rock & static_objects:
                        rock = move_right(rock)
            elif wind[w] == ">":
                if not any([x == RIGHT_LIMIT for (x, y) in rock]):
                    rock = move_right(rock)
                    if rock & static_objects:
                        rock = move_left(rock)
            wind_idx += 1
            # print_world(static_objects, rock)
            # Drop
            if not any([y == 0 for (x, y) in rock]):
                rock = move_down(rock)
                if rock & static_objects:
                    rock = move_up(rock)
                    moving = False
            else:
                moving = False

            if not moving:
                for (x, y) in rock:
                    static_objects.add((x, y))
                max_y = max([y for (x, y) in static_objects])

                sig = (w, s, create_world_sig(static_objects))
                if sig in seen:
                    (old_t, old_y) = seen[sig]
                    dt = t - old_t
                    dy = max_y - old_y
                    chunk = (max_t - t) // dt
                    skipped += chunk * dy
                    t += chunk * dt

                    assert t <= max_t

                seen[sig] = (t, max_y)
            # print_world(static_objects, rock)

        shape_idx += 1

    return max_y + 1 + skipped


def pt1(raw_input: Path):
    """part 1"""
    return run(wind=raw_input.read_text(encoding="utf-8"), max_t=2022)


def pt2(raw_input: Path):
    """part 2"""
    return run(wind=raw_input.read_text(encoding="utf-8"), max_t=1000000000000)
