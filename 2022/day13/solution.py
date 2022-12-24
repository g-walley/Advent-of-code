from collections import deque
from pathlib import Path
from typing import Deque, List
from functools import cmp_to_key


def get_next(d: Deque):
    item: str = d.popleft()
    if d:
        if item.isdigit() and d[0] == "0":
            item += d.popleft()
    return item


def compare(left: str, right: str) -> int:
    left, right = (
        deque([char for char in left]),
        deque([char for char in right]),
    )
    while left and right:
        l = get_next(left)
        r = get_next(right)
        if l == r:
            continue
        elif (
            l.isdigit() and r.isdigit()
        ):  # Left side is smaller, or right side is smaller
            return int(l) - int(r)

        if (l == "]" and (r == "," or r == "[")) or (
            l == "]" and r.isdigit()
        ):  # Left ran out of items
            return -1
        elif ((l == "," or l == "[") and r == "]") or (
            l.isdigit() and r == "]"
        ):  # Right ran out of items
            return 1
        elif l == "[" and r != "[":  # Convert right digit into a list
            right.extendleft(["]", r])
        elif l != "[" and r == "[":  # Convert left digit into a list
            left.extendleft(["]", l])

    return 0


def pt1(raw_input: Path) -> int:
    """part 1"""
    total = 0
    for idx, pair in enumerate(raw_input.read_text().split("\n\n"), start=1):
        lines = pair.splitlines()
        left, right = (
            deque([char for char in lines[0]]),
            deque([char for char in lines[1]]),
        )

        if compare(left, right) < 0:
            total += idx

    return total


def pt2(raw_input: Path):
    """part 2"""
    file_as_list: List[str] = raw_input.read_text().replace("\n\n", "\n").splitlines()
    file_as_list.extend(["[[2]]", "[[6]]"])

    sorted_list: List = sorted(file_as_list, key=cmp_to_key(compare))

    return (sorted_list.index("[[2]]") + 1) * (sorted_list.index("[[6]]") + 1)
