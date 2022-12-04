import re
from typing import Callable
def matcher(raw_input: str, comp: Callable):
    """shared code for both parts"""
    count = 0
    re_pattern = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    for row in raw_input.splitlines():
        if comp(*tuple([int(i) for i in re_pattern.match(row).group(1, 2, 3, 4)])):
            count += 1
    return count

def pt1(raw_input: str):
    """part 1"""
    def comp(x1, y1, x2, y2):
        return True if (x2 <= x1 and y1 <= y2) or (x1 <= x2 and y2 <= y1) else False
    return matcher(raw_input, comp)

def pt2(raw_input):
    """part 2"""
    def comp(x1, y1, x2, y2):
        return True if (x1 <= y2 and x2 <= y1) else False
    return matcher(raw_input, comp)
