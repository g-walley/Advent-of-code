from collections import deque
import re
from typing import Callable, Dict, Deque, Iterable


def build_stacks(in_crates: str)-> Dict[str, Deque]:
    """Builds the crate stack dictionary"""
    in_crates: Iterable[str] = in_crates.splitlines()
    in_crates.reverse()

    # create a dictionary mapping of positions to column names
    col_positions = {p: col for p, col in enumerate(in_crates.pop(0)) if col != ' '}

    # initialise deque objects
    stacks : Dict[str, Deque] = {col: deque() for col in col_positions.values()}

    for level in in_crates:
        for p, col in enumerate(level):
            if p in col_positions and col != ' ':
                stacks[col_positions[p]].append(col)

    return stacks

def move_crates(stacks: Dict[str, Deque], instructions: str, crane: Callable):
        # move crates between stacks:
    re_instr = re.compile(r'move (?P<move>\d+) from (?P<from>\d+) to (?P<to>\d+)')

    for line in instructions.splitlines():
        instr: Dict = re_instr.search(line).groupdict()
        crane(stacks, instr)

def pt1(in_crates: str, in_instr: str):
    """part 1"""

    def pt1_crane(stacks: Dict[str, Deque], instr: Dict):
        for _ in range(int(instr['move'])):
            crate = stacks[instr['from']].pop()
            stacks[instr['to']].append(crate)

    move_crates(stacks := build_stacks(in_crates), in_instr, pt1_crane)

    return ''.join([stack.pop() for stack in stacks.values()])

def pt2(in_crates: str, in_instr: str):
    """part 2"""
    def pt2_crane(stacks: Dict[str, Deque], instr: Dict):
        crane_grabber = deque()
        for _ in range(int(instr['move'])):
            crane_grabber.appendleft(stacks[instr['from']].pop())
        while crane_grabber:
            stacks[instr['to']].append(crane_grabber.popleft())

    move_crates(stacks := build_stacks(in_crates), in_instr, pt2_crane)
    return ''.join([stack.pop() for stack in stacks.values()])
