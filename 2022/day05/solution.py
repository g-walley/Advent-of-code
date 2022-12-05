from collections import deque
import re
from typing import Dict, Deque, Iterable


def build_stacks(in_crates: str):
    """Builds the crate stack dictionary"""
    in_crates: Iterable[str] = in_crates.splitlines()
    in_crates.reverse()

    # create a dictionary mapping of positions to column names
    col_positions = {
        p: col
        for p, col in enumerate(in_crates.pop(0))
        if col != ' '
    }
    # initialise deque objects
    stacks : Dict[str, Deque] = {
        col: deque()
        for col in col_positions.values()
    }

    for level in in_crates:
        for p, col in enumerate(level):
            char_num = ord(col)
            if 65 < char_num and char_num < 91:
                stacks[col_positions[p]].append(col)

    return stacks

def pt1(in_crates: str, in_instr: str):
    """part 1"""
    stacks = build_stacks(in_crates)

    # move crates between stacks:
    re_instr = re.compile(r'move (?P<move>\d+) from (?P<from>\d+) to (?P<to>\d+)')

    for line in in_instr.splitlines():
        instr: Dict = re_instr.search(line).groupdict()
        for _ in range(int(instr['move'])):
            crate = stacks[instr['from']].pop()
            stacks[instr['to']].append(crate)

    return ''.join([
        stack.pop()
        for stack in stacks.values()
    ])

def pt2(in_crates: str, in_instr: str):
    """part 2"""
    stacks = build_stacks(in_crates)
    crane = deque()
    # move crates between stacks:
    re_instr = re.compile(r'move (?P<move>\d+) from (?P<from>\d+) to (?P<to>\d+)')
    for line in in_instr.splitlines():
        instr: Dict = re_instr.search(line).groupdict()
        for _ in range(int(instr['move'])):
            crane.appendleft(stacks[instr['from']].pop())
        while crane:
            stacks[instr['to']].append(crane.popleft())

    return ''.join([
        stack.pop()
        for stack in stacks.values()
    ])

