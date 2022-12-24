from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def __add__(self, other: Point2D):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D):
        return Point2D(self.x - other.x, self.y - other.y)

    def __floordiv__(self, other: Point2D):
        x = self.x // other.x if self.x != 0 else 0
        y = self.y // other.y if self.y != 0 else 0
        return Point2D(x, y)


@dataclass(frozen=True)
class Direction(Point2D):
    ...


@dataclass(frozen=True)
class Axis:
    min: int
    max: int


@dataclass
class Cave:
    x_axis: Axis = Axis(0, 0)
    y_axis: Axis = Axis(0, 0)
    known: Dict[Point2D, str] = field(default_factory=dict)

    def import_terrain(self, file: Path) -> Dict[Point2D, str]:

        for row in file.read_text(encoding="utf-8").splitlines():
            pivots = [
                Point2D(int(row.split(",")[0]), int(row.split(",")[1]))
                for row in row.split(" -> ")
            ]
            self.known[pivots[0]] = "#"
            for idx, pivot in enumerate(pivots[:-1]):
                diff = pivots[idx + 1] - pivot
                direction = diff // Point2D(abs(diff.x), abs(diff.y))
                crosshair = Point2D(pivot.x, pivot.y)

                while crosshair != pivots[idx + 1]:
                    crosshair = crosshair + direction
                    self.known[crosshair] = "#"

        self.known[Point2D(500, 0)] = "+"

    def update_boundaries(self):
        all_x = [point.x for point in self.known]
        all_y = [point.y for point in self.known if self.known[point] == "#"]
        all_y.append(0)

        self.x_axis = Axis(min(all_x), max(all_x))
        self.y_axis = Axis(min(all_y), max(all_y))

    def draw(self, sand: Optional[Point2D] = None):
        print(f"x: {self.x_axis}, y: {self.y_axis}")

        for y in range(self.y_axis.min, self.y_axis.max + 2):
            line = f"{y} \t"
            for x in range(self.x_axis.min - 1, self.x_axis.max + 2):
                if (p := Point2D(x, y)) == sand:
                    line += "0"
                else:
                    line += self.known.get(p, ".")
            print(line)

    def drop_sand(self, floor: Optional[bool] = False) -> bool:
        moving = True
        location = Point2D(500, 0)
        deltas = [Direction(0, 1), Direction(-1, 1), Direction(1, 1)]

        while moving:
            for delta in deltas:
                new_location = location + delta
                if floor and new_location.y >= self.y_axis.max + 2:
                    self.known[location] = "o"
                    moving = False
                    break
                elif new_location in self.known:
                    continue
                else:
                    if (not floor) and (location.y >= self.y_axis.max):
                        return False
                    location = new_location
                    break
            else:
                self.known[location] = "o"
                moving = False

                if floor and location == Point2D(500, 0):
                    return False
            self.update_boundaries()
            # self.draw(location)
        return True


def pt1(raw_input: Path):
    """part 1"""
    cave = Cave()
    cave.import_terrain(raw_input)
    cave.draw()

    counter = 0
    while cave.drop_sand():
        counter += 1

    cave.draw()
    return counter


def pt2(raw_input: Path):
    """part 2"""

    cave = Cave()
    cave.import_terrain(raw_input)

    counter = 0
    while cave.drop_sand(floor=True):
        counter += 1
        if counter % 100 == 0:
            cave.draw()

    cave.draw()
    return counter + 1
