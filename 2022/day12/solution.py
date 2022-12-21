from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int
    def __add__(self, other: Point2D):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D):
        return Point2D(self.x - other.x, self.y - other.y)


@dataclass
class GeoData:
    height: int
    distance: int
    end: bool


@dataclass(frozen=True)
class Direction(Point2D):
    ...


directions = {
    Direction(0, -1),
    Direction(0, 1),
    Direction(1, 0),
    Direction(-1, 0),
}


@dataclass
class Map:
    locations: Dict[Point2D, GeoData] = field(default_factory=dict)

    def adjacent(self, location: Point2D) -> List[Point2D]:
        return [
            location + direction
            for direction in directions
            if (location + direction) in self.locations
        ]


def pt1(raw_input: Path):
    """part 1"""
    map_locations: Dict[Point2D: GeoData] = {}
    map_str = raw_input.read_text(encoding='utf-8')

    for y, line in enumerate(map_str.splitlines()):
        for x, height_str in enumerate(line):
            if height_str == 'S':
                geo_data = GeoData(-1, 0, False)
            elif height_str == 'E':
                geo_data = GeoData(height=ord('z') - ord('a'), distance=-1, end=True)
            else:
                geo_data = GeoData(height=ord(height_str) - ord('a'), distance=-1, end=False)

            map_locations[Point2D(x, y)] = geo_data

    map = Map(map_locations)

    for i in range(len(map_locations)):
        next_points = [location for location, geo in map.locations.items() if geo.distance == i]
        for point in next_points:
            for adjacent in map.adjacent(point):
                if (map.locations[adjacent].distance == -1) and (
                    map.locations[adjacent].height <= map.locations[point].height + 1
                ):
                    map.locations[adjacent].distance = i + 1

            if map.locations[point].end:
                return i


def pt2(raw_input: Path):
    """part 2"""

    map_locations: Dict[Point2D: GeoData] = {}
    map_str = raw_input.read_text(encoding='utf-8')

    for y, line in enumerate(map_str.splitlines()):
        for x, height_str in enumerate(line):
            if height_str == 'S':
                geo_data = GeoData(-1, -1, True)
            elif height_str == 'E':
                geo_data = GeoData(height=ord('z') - ord('a'), distance=0, end=False)
            elif height_str == 'a':
                geo_data = GeoData(height=0, distance=-1, end=True)
            else:
                geo_data = GeoData(height=ord(height_str) - ord('a'), distance=-1, end=False)

            map_locations[Point2D(x, y)] = geo_data

    map = Map(map_locations)

    a_not_found = True
    i = 0
    while a_not_found:
        next_points = [location for location, geo in map.locations.items() if geo.distance == i]
        for point in next_points:
            for adjacent in map.adjacent(point):
                if (map.locations[adjacent].distance == -1) and (
                    map.locations[adjacent].height >= map.locations[point].height - 1
                ):
                    map.locations[adjacent].distance = i + 1
                    if map.locations[adjacent].height == 0:
                        a_not_found = False
        i += 1
    return min([map.locations[point].distance for point, geo in map.locations.items() if geo.distance != -1 and geo.height == 0])