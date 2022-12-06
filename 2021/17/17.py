import numpy as np
import re
from pathlib import Path
from collections import namedtuple

REGEX = (
    r"target area: "
    r"x=(?P<x_min>-?\d*)..(?P<x_max>-?\d*), "
    r"y=(?P<y_min>-?\d*)..(?P<y_max>-?\d*)\n"
)

Point = namedtuple("Point", ("x", "y"))


def in_target(target, ball_pos: Point):
    return (
        int(target["x_min"]) <= ball_pos.x <= int(target["x_max"]) and
        int(target["y_min"]) <= ball_pos.y <= int(target["y_max"])
    )

def pt1(target) -> np.int64:
    """Part 1"""
    y_vel = (int(target["y_min"]) + 1) * -1
    y_displacement = 0
    while y_vel > 0:
        y_displacement += y_vel
        y_vel -= 1
    return y_displacement


def pt2(target) -> np.int64:
    """Part 2"""
    velocities = []
    y_min_vel = int(target["y_min"])
    y_max_vel = abs(int(target["y_min"]) + 1)
    x_min_vel = 0
    x_pos = 0
    while x_pos <= int(target["x_min"]):
        x_min_vel += 1
        x_pos += x_min_vel
    x_max_vel = int(target["x_max"])
    print(f"x_vel: {x_min_vel}->{x_max_vel}; y_vel: {y_min_vel}->{y_max_vel}")
    for init_x_vel in range(x_max_vel + 1):
        for init_y_vel in range(y_min_vel, y_max_vel + 1):
            pos = Point(0, 0)
            x_vel = init_x_vel
            y_vel = init_y_vel
            while pos.x <= int(target["x_max"]) and int(target["y_min"]) <= pos.y:
                pos = Point(pos.x + x_vel, pos.y + y_vel)
                if x_vel > 0:
                    x_vel -= 1
                y_vel -= 1

                if in_target(target, pos):
                    velocities.append((init_x_vel, init_y_vel))
                    break
    return len(velocities)

if __name__ == "__main__":
    ex_in = re.match(REGEX, Path("./17/ex.txt").read_text(encoding="utf-8"))
    ex1=pt1(ex_in.groupdict())
    print(f"ex1: {ex1}")
    my_in = re.match(REGEX, Path("./17/input.txt").read_text(encoding="utf-8"))
    p1=pt1(my_in.groupdict())
    print(f"part1: {p1}")
    ex2=pt2(ex_in)
    print(f"ex2: {ex2}")
    p2=pt2(my_in)
    print(f"part2: {p2}")
