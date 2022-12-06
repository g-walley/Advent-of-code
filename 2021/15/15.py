from typing import List
import numpy as np
from asyncio import PriorityQueue
from pathlib import Path
from collections import namedtuple
from time import time
from functools import wraps

def timing(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start = time()
        result = method(*args, **kwargs)
        end = time()
        print(f"Elapsed time: {end-start}")
        return result
    return wrapper


Point = namedtuple("point", ("x", "y"))
QData = namedtuple("QData", ("prio", "point"))

@timing
def pt1(input_file) -> np.int64:
    """Part 1"""
    lines = Path(input_file).read_text(encoding="utf-8").splitlines()
    grid = [[int(char) for char in line] for line in lines]
    start = Point(0,0)
    end = Point(len(grid) - 1, len(grid[0]) - 1)
    que = PriorityQueue(maxsize=0)
    all_points = {
        Point(x, y): {
            "dist": np.nan,
            "via": None
        }
        for x in range(end.x + 1)
        for y in range(end.y + 1)
    }
    all_points[(0,0)]["dist"] = 0

    que.put_nowait(QData(np.float64(0), start))

    visited = set()
    while not que.empty():
        p_data: QData = que.get_nowait()
        point: Point = p_data.point
        distance = p_data.prio
        visited.add(point)

        points_to_add: List[QData] = []

        def add_point(p):
            if p not in visited:
                new_dist = distance + np.float64(grid[p.x][p.y])
                points_to_add.append((new_dist, p))
        # right
        if point.x < end.x:
            add_point(Point(point.x + 1, point.y))
        # up
        if point.y != 0:
            add_point(Point(point.x, point.y - 1))
        # left
        if point.x != 0:
            add_point(Point(point.x - 1, point.y))
        # down
        if point.y < end.y:
            add_point(Point(point.x, point.y + 1))

        for new_dist, p in points_to_add:
            old_dist = all_points[p]["dist"]
            if new_dist < old_dist or old_dist is np.nan:
                all_points[p]["via"] = p
                all_points[p]["dist"] = new_dist
                que.put_nowait(QData(new_dist, p))
        que.task_done()
    return all_points[end]["dist"]

@timing
def pt2(input_file, size) -> np.int64:
    """Part 2"""
    def extend_grid(new, grid, axis):
        for _ in range(size - 1):
            new = np.mod(new + 1, 10)
            np.add.at(new, np.equal(new, 0), 1)
            grid = np.concatenate((grid, new), axis=axis)
        return grid

    lines = Path(input_file).read_text(encoding="utf-8").splitlines()
    grid = np.array([[int(char) for char in line] for line in lines])

    new_grid = grid
    grid = extend_grid(new_grid, grid, axis=0)
    new_grid = grid
    grid = extend_grid(new_grid, grid, axis=1)

    start = Point(0,0)
    end = Point(len(grid) - 1, len(grid[0]) - 1)
    que = PriorityQueue(maxsize=0)
    all_points = {
        Point(x, y): {
            "dist": np.nan,
            "via": None
        }
        for x in range(end.x + 1)
        for y in range(end.y + 1)
    }
    all_points[(0,0)]["dist"] = 0

    que.put_nowait(QData(np.float64(0), start))

    visited = set()
    while not que.empty():
        p_data: QData = que.get_nowait()
        point: Point = p_data.point
        distance = p_data.prio
        visited.add(point)

        points_to_add: List[QData] = []

        def add_point(p):
            if p not in visited:
                new_dist = distance + np.float64(grid[p.x][p.y])
                points_to_add.append((new_dist, p))
        # right
        if point.x < end.x:
            add_point(Point(point.x + 1, point.y))
        # up
        if point.y != 0:
            add_point(Point(point.x, point.y - 1))
        # left
        if point.x != 0:
            add_point(Point(point.x - 1, point.y))
        # down
        if point.y < end.y:
            add_point(Point(point.x, point.y + 1))

        for new_dist, p in points_to_add:
            old_dist = all_points[p]["dist"]
            if new_dist < old_dist or old_dist is np.nan:
                all_points[p]["via"] = p
                all_points[p]["dist"] = new_dist
                que.put_nowait(QData(new_dist, p))
        que.task_done()
    return all_points[end]["dist"]

if __name__ == "__main__":
    ex1=pt1("./15/ex.txt")
    print(f"ex1: {ex1}")
    p1=pt1("./15/input.txt")
    print(f"part1: {p1}")
    ex2=pt2("./15/ex.txt", 5)
    print(f"ex2: {ex2}")
    p2=pt2("./15/input.txt", 5)

    print(f"part2: {p2}")
