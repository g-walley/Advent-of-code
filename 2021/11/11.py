import numpy as np
from copy import deepcopy

def flash(grid, row, col, flash_count):
    flash_count += 1
    grid[row, col] = -100
    for row_idx in range(row - 1, row + 2):
        for col_idx in range(col - 1, col + 2):
            if row_idx == row and col_idx == col:
                continue
            if 0 <= row_idx < len(grid) and 0 <= col_idx < len(grid[row_idx]):
                grid[row_idx, col_idx] += 1
                if grid[row_idx, col_idx] >= 10:
                    flash_count = flash(grid, row_idx, col_idx, flash_count)

    return flash_count


def step(grid, flash_count):
    grid += 1

    for row_idx, row in enumerate(grid):
        for col_idx, val in enumerate(row):
            if val >= 10:
                flash_count = flash(grid, row_idx, col_idx, flash_count)

    for row_idx, row in enumerate(grid):
        for col_idx, val in enumerate(row):
            if val < 0:
                grid[row_idx, col_idx] = 0

    return flash_count


def pt1(grid) -> np.int64:
    """Part 1"""
    flash_count = 0
    for _ in range(100):
        flash_count = step(grid, flash_count)

    return flash_count

def pt2(grid) -> np.int64:
    """Part 2"""
    flash_count = 0
    loop_count = 0
    zeros = np.zeros_like(grid)

    while True:
        flash_count = step(grid, flash_count)
        loop_count += 1
        if np.equal(zeros, grid).all():
            break

    return loop_count

if __name__ == "__main__":
    ex_in = np.genfromtxt("11/example.txt", dtype=int)
    my_in = np.genfromtxt("11/input.txt", dtype=int)
    ex1=pt1(deepcopy(ex_in))
    p1=pt1(deepcopy(my_in))
    ex2=pt2(deepcopy(ex_in))
    p2=pt2(deepcopy(my_in))

    print(f"ex1: {ex1}")
    print(f"part1: {p1}")
    print(f"ex2: {ex2}")
    print(f"part2: {p2}")
