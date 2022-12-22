from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from ast import literal_eval
from typing import List


@dataclass
class Pair:
    left: List[int | List]
    right: List[int | List]


def compare_lists(left: List, right: List) -> bool:

    print(f"{left}\n{right}\n\n")


def right_side_is_smaller(pair: Pair) -> bool:
    if isinstance(pair.left, list) and isinstance(pair.right, int):
        pair.right = [pair.right]

    if isinstance(pair.left, int) and isinstance(pair.right, list):
        pair.left = [pair.left]

    assert isinstance(pair.left, list), "Left is not list"
    assert isinstance(pair.right, list), "Right is not list"

    while pair.left:
        left_elem = pair.left.pop(0)

        try:
            right_elem = pair.right.pop(0)
        except IndexError:
            return False  # Right side ran out of items, so inputs are _not_ in the right order

        if isinstance(left_elem, list) or isinstance(right_elem, list):
            if right_side_is_smaller(Pair(left_elem, right_elem)):
                return True
        elif isinstance(left_elem, int) and isinstance(right_elem, int):
            if
        else:
            assert False, "Neither are int or list!!!"




def pt1(raw_input: Path) -> int:
    """part 1"""
    total = 0
    for idx, pair in enumerate(raw_input.read_text().split("\n\n"), start=1):
        lines = pair.splitlines()
        pair = Pair(literal_eval(lines[0]), literal_eval(lines[1]))
        if right_side_is_smaller(pair):
            total += idx

    return total


def pt2(raw_input):
    """part 2"""
