import pathlib
import numpy as np
from typing import NamedTuple


class Coordinate(NamedTuple):
    """coordinate (x,y)"""
    x: int
    y: int


class Line():
    def __init__(self, line_str: str):
        spl = line_str.split(" -> ")
        self.start = Coordinate(*tuple(self.gen_coords(spl[0])))
        self.end = Coordinate(*tuple(self.gen_coords(spl[1])))

    def __repr__(self):
        return f"({self.start.x},{self.start.y}) -> ({self.end.x},{self.end.y}) | len: {self.length} | vertical: {self.vertical} | horizontal: {self.horizontal}"

    @staticmethod
    def gen_coords(coord_str) -> int:
        """_"""
        for val in coord_str.split(","):
            yield int(val)

    @property
    def horizontal(self) -> bool:
        """Returns True if line is horizontal"""
        return self.start.y == self.end.y

    @property
    def vertical(self) -> bool:
        """Returns True if line is vertical"""
        return self.start.x == self.end.x

    @property
    def maximum_x(self) -> int:
        """Max of start.x and end.x"""
        return max(self.start.x, self.end.x)

    @property
    def maximum_y(self) -> int:
        """Max of start.y and end.y"""
        return max(self.start.y, self.end.y)

    @property
    def length(self) -> np.int64:
        """length of line, inclusive"""
        if self.horizontal:
            return self.end.x - self.start.x
        elif self.vertical:
            return self.end.y - self.start.y
        else:
            return self.end.x - self.start.x

    @property
    def x_dir(self) -> int:
        """x direction"""
        return 1 if self.start.x <= self.end.x else -1

    @property
    def y_dir(self) -> int:
        """x direction"""
        return 1 if self.start.y <= self.end.y else -1

    def all_coords(self):
        """generates all coordinates from start to end"""
        for i in range(abs(self.length) + 1):
            if self.horizontal:
                yield Coordinate(
                    self.start.x + i*self.x_dir,
                    self.start.y)
            elif self.vertical:
                yield Coordinate(
                    self.start.x,
                    self.start.y + i*self.y_dir)
            else:
                yield Coordinate(
                    self.start.x + i*self.x_dir,
                    self.start.y + i*self.y_dir)


def pt1(input: str) -> int:
    """Part 1"""
    input_file = pathlib.Path(input)
    lines = [
        Line(line_str)
        for line_str in input_file.read_text(
            encoding="utf-8").splitlines()
    ]
    max_x = 0
    max_y = 0
    for line in lines:
        max_x = max(max_x, line.maximum_x)
        max_y = max(max_y, line.maximum_y)

    # X is row, Y is column
    grid = np.zeros(
        dtype=np.int64,
        shape=(max_x + 1, max_y + 1)
    )

    for line in lines:
        for coord in line.all_coords():
            grid[coord.x, coord.y] += 1

    unique, counts = np.unique(grid, return_counts=True)
    count_of_each_num = dict(zip(unique, counts))

    total = 0
    for num, count in count_of_each_num.items():
        if num >= 2:
            total += count
    return total


def pt2() -> int:
    """Part 2"""

    return 0


if __name__ == "__main__":
    ex = pt1("./5/example_input.txt")
    p1 = pt1("./5/input.txt")
    p2 = pt2()

    print(f"ex pt1: {ex}")
    print(f"part1: {p1}")
    print(f"part2: {p2}")
