from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Set
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


@dataclass(frozen=True)
class Axis:
    min: int
    max: int


def adjacent_free_voxels(raw_input: Path) -> Dict[Point3D, int]:
    surfaces: Dict[Point3D, Set] = {}
    for line in raw_input.read_text(encoding="utf-8").splitlines():
        parsed = parse("{x:d},{y:d},{z:d}", line)
        cube_loc = Point3D(parsed["x"], parsed["y"], parsed["z"])
        surface_faces = {cube_loc + direction for direction in directions}
        for adj in list(surface_faces):
            if surfaces.get(adj, None):
                surfaces[adj].remove(cube_loc)
                surface_faces.remove(adj)
        surfaces[cube_loc] = surface_faces

    return surfaces


def pt1(raw_input: Path):
    """part 1"""
    surfaces = adjacent_free_voxels(raw_input)
    return sum([len(adj) for adj in surfaces.values()])


def pt2(raw_input: Path):
    """part 2"""
    surfaces = adjacent_free_voxels(raw_input)
    # surfaces = {k: v for k, v in adjacent_free_voxels(raw_input).items() if len(v)}
    all_x = [cube.x for cube in surfaces]
    all_y = [cube.y for cube in surfaces]
    all_z = [cube.z for cube in surfaces]

    x_axis = Axis(min(all_x) - 2, max(all_x) + 2)
    y_axis = Axis(min(all_y) - 2, max(all_y) + 2)
    z_axis = Axis(min(all_z) - 2, max(all_z) + 2)
    count = 0
    unchecked_cubes = {Point3D(x_axis.min, y_axis.min, z_axis.min)}
    checked_cubes = set()
    while unchecked_cubes:
        for unchecked_cube in list(unchecked_cubes):
            adj_cubes = [unchecked_cube + direction for direction in directions]
            cubes_to_add = [
                adj
                for adj in adj_cubes
                if adj not in surfaces
                and adj not in checked_cubes
                and (x_axis.min <= adj.x and adj.x <= x_axis.max)
                and (y_axis.min <= adj.y and adj.y <= y_axis.max)
                and (z_axis.min <= adj.z and adj.z <= z_axis.max)
            ]
            for cube in cubes_to_add:
                unchecked_cubes.add(cube)

            for adj in adj_cubes:
                if adj in surfaces:
                    count+=1
            unchecked_cubes.remove(unchecked_cube)
            checked_cubes.add(unchecked_cube)

    return count
