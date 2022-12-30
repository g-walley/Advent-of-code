from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict
from parse import parse


@dataclass(frozen=True)
class Point3D:
    x: int
    y: int
    z: int
    def __add__(self, other: Point3D):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Point3D):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)


directions = [
    Point3D(0, 0, 1),
    Point3D(0, 1, 0),
    Point3D(1, 0, 0),
    Point3D(0, 0, -1),
    Point3D(0, -1, 0),
    Point3D(-1, 0, 0),
]


class Adjacent:
    x_p: bool
    x_n: bool
    y_p: bool
    y_n: bool
    z_p: bool
    z_n: bool


@dataclass
class LavaCube:
    pos: Point3D
    adj: Adjacent



def pt1(raw_input: Path):
    """part 1"""
    cube_side_showing: Dict[Point3D, int] = {}
    for line in raw_input.read_text(encoding='utf-8').splitlines():
        parsed = parse("{x:d},{y:d},{z:d}", line)
        cube_loc = Point3D(parsed["x"], parsed["y"], parsed["z"])
        sides = 6
        for direction in directions:
            adj_cube_loc = cube_loc + direction
            if cube_side_showing.get(adj_cube_loc, None):
                cube_side_showing[adj_cube_loc] -= 1
                sides -= 1
        cube_side_showing[cube_loc] = sides
    return sum(cube_side_showing.values())





def pt2(raw_input: Path):
    """part 2"""