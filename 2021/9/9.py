import numpy as np
from collections import namedtuple

Point = namedtuple("Point", ["row", "col"])

def pt1(grid: np.ndarray) -> np.int64:
    """Part 1"""
    shape = grid.shape
    low_points = []
    score: np.int64 = 0
    for row_i, row in enumerate(grid):
        for col_i, val in enumerate(row):
            if row_i != 0 and (grid[row_i - 1, col_i] <= val):
                above = False
            else:
                above = True

            if row_i != (shape[0] - 1) and (grid[row_i + 1, col_i] <= val):
                below = False
            else:
                below = True

            if col_i != 0 and (grid[row_i, col_i - 1] <= val):
                left = False
            else:
                left = True

            if col_i != (shape[1] - 1) and (grid[row_i, col_i + 1] <= val):
                right = False
            else:
                right = True

            if above and below and left and right:
                low_points.append((row_i, col_i))
                score += val + 1

    return score

def pt2(grid: np.ndarray) -> np.int64:
    """Part 2"""

    shape = grid.shape
    low_points = []
    score = np.int64(0)
    for row_i, row in enumerate(grid):
        for col_i, val in enumerate(row):
            if row_i != 0 and (grid[row_i - 1, col_i] <= val):
                above = False
            else:
                above = True

            if row_i != (shape[0] - 1) and (grid[row_i + 1, col_i] <= val):
                below = False
            else:
                below = True

            if col_i != 0 and (grid[row_i, col_i - 1] <= val):
                left = False
            else:
                left = True

            if col_i != (shape[1] - 1) and (grid[row_i, col_i + 1] <= val):
                right = False
            else:
                right = True

            if above and below and left and right:
                low_points.append(Point(row_i, col_i))

    basin_sizes = []
    for point in low_points:
        points_to_check = [point]
        points_already_checked = []
        size = 0
        while points_to_check:
            p2c = points_to_check.pop()
            if p2c not in points_already_checked:
                size += 1
                above_p = Point(p2c.row - 1, p2c.col) if p2c.row != 0 else None
                below_p = Point(p2c.row + 1, p2c.col) if p2c.row != grid.shape[0] - 1 else None
                left_p = Point(p2c.row, p2c.col - 1) if p2c.col != 0 else None
                right_p = Point(p2c.row, p2c.col + 1) if p2c.col != grid.shape[1] - 1 else None

                if above_p and grid[above_p.row, above_p.col] != 9:
                    points_to_check.append(above_p)

                if below_p and grid[below_p.row, below_p.col] != 9:
                    points_to_check.append(below_p)

                if left_p and grid[left_p.row, left_p.col] != 9:
                    points_to_check.append(left_p)

                if right_p and grid[right_p.row, right_p.col] != 9:
                    points_to_check.append(right_p)

                points_already_checked.append(p2c)

        basin_sizes.append(size)

    basin_sizes.sort()

    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes [-3]

if __name__ == "__main__":
    ex_in = np.genfromtxt("9/ex.txt", dtype=int)
    my_in = np.genfromtxt("9/input.txt", dtype=int)
    ex1=pt1(ex_in)
    p1=pt1(my_in)
    ex2=pt2(ex_in)
    p2=pt2(my_in)

    print(f"ex1: {ex1}")
    print(f"part1: {p1}")
    print(f"ex2: {ex2}")
    print(f"part2: {p2}")
