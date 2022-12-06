from typing import List
import numpy as np
from collections import namedtuple

Hole = namedtuple("Hole", ["x", "y"])

def print_out(grid):
    print_str = ""
    for row in grid:
        for elem in row:
            if elem:
                print_str += "#"
            else:
                print_str += "."
        print_str += "\n"
    return print_str


def fold(grid, instr):
    if instr[0] == "y":
        sec_1 = grid[:, 0:instr[1]]
        sec_2 = grid[:, instr[1] + 1:]
        for y_idx in range(len(sec_2[0])):
            sec_1[:, len(sec_1[0]) - 1 - y_idx] = np.logical_or(
                sec_1[:, len(sec_1[0]) - 1 - y_idx], sec_2[:, y_idx])
        return sec_1

    if instr[0] == "x":
        sec_1 = grid[0:instr[1], :]
        sec_2 = grid[instr[1] + 1:, :]
        for row_idx, sec_2_row in enumerate(sec_2):
            sec_1_row = sec_1[len(sec_1) - 1 - row_idx, :]
            sec_1[len(sec_1) - 1 - row_idx, :] = np.logical_or(
                sec_1_row, sec_2_row)
        return sec_1


def pt1(holes: List[str], fold_list) -> np.int64:
    """Part 1"""
    max_x = np.max(holes[:, 0])
    max_y = np.max(holes[:, 1])
    shape = (max_x + 1, max_y + 1)
    grid = np.full(
        shape=shape,
        fill_value=False,
        dtype=bool,
    )
    for hole in holes:
        grid[hole[0], hole[1]] = True

    folded = fold(grid, fold_list[0])
    return np.count_nonzero(folded)

def pt2(holes, fold_list) -> np.int64:
    """Part 2"""
    max_x = np.max(holes[:, 0])
    max_y = np.max(holes[:, 1])
    shape = (max_x + 1, max_y + 1)
    grid = np.full(
        shape=shape,
        fill_value=False,
        dtype=bool,
    )
    for hole in holes:
        grid[hole[0], hole[1]] = True

    for f in fold_list:
        grid = fold(grid, f)
    return print_out(np.transpose(grid))

if __name__ == "__main__":
    # ex1_in = Path("./13/ex1.txt").read_text(encoding="utf-8").splitlines()
    ex1_in = np.genfromtxt("13/ex1.txt", dtype=int, delimiter=",")
    folds = [("y", 7), ("x", 5)]
    ex1=pt1(ex1_in, folds)
    my_in = np.genfromtxt("13/input.txt", dtype=int, delimiter=",")
    folds = [
        ("x", 655),
        ("y", 447),
        ("x", 327),
        ("y", 223),
        ("x", 163),
        ("y", 111),
        ("x", 81),
        ("y", 55),
        ("x", 40),
        ("y", 27),
        ("y", 13),
        ("y", 6),
    ]
    p1=pt1(my_in, folds)
    p2=pt2(my_in, folds)

    print(f"ex1: {ex1}")
    print(f"part1: {p1}")
    print(f"part2:\n{p2}")
