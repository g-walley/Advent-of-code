from typing import Dict, Set
import numpy as np
from pathlib import Path

ZERO = 6
ONE = 2
TWO = 5
THREE = 5
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 3
EIGHT = 7
NINE = 6

def pt1(display_data) -> np.int64:
    """Part 1"""
    notes = Path(display_data).read_text(encoding="utf-8").splitlines()
    output = [line.split(" | ")[1] for line in notes]
    output = [line.split(" ") for line in output]

    count = 0
    for line in output:
        for elem in line:
            l = len(elem)
            if l == ONE or l == FOUR or l == SEVEN or l == EIGHT:
                count += 1
    return count

def pt2(display_data) -> int:
    """Part 2"""
    def add_pattern_to_map(mapping, pattern, first_pass=True):
        pattern_set = frozenset(pattern)
        length = len(pattern_set)
        if first_pass:
            if length == 2:
                mapping['1'] = pattern_set
            elif length == 3:
                mapping['7'] = pattern_set
            elif length == 4:
                mapping['4'] = pattern_set
            elif length == 7:
                mapping['8'] = pattern_set
        else:
            if length == 5:
                int_len = len(pattern_set.intersection(mapping['4']))
                if int_len == 3:
                    int_len = len(pattern_set.intersection(mapping['1']))
                    if int_len == 2:
                        mapping['3'] = pattern_set
                    elif int_len == 1:
                        mapping['5'] = pattern_set
                elif int_len == 2:
                    mapping['2'] = pattern_set
            elif length == 6:
                int_len = len(pattern_set.intersection(mapping['7']))
                if int_len == 2:
                    mapping['6'] = pattern_set
                else:
                    int_len = len(pattern_set.intersection(mapping['4']))
                    if int_len == 4:
                        mapping['9'] = pattern_set
                    elif int_len == 3:
                        mapping['0'] = pattern_set

    notes = Path(display_data).read_text(encoding="utf-8").splitlines()
    split_notes = [line.split(" | ") for line in notes]
    sig_patterns = [line[0].split(" ") for line in split_notes]
    outputs = [line[1].split(" ") for line in split_notes]


    values = []
    for index, line in enumerate(sig_patterns):
        mapping: Dict[int, Set] = {}

        for pattern in line:
            add_pattern_to_map(mapping, pattern)

        for pattern in line:
            add_pattern_to_map(mapping, pattern, first_pass=False)

        output_map = {v: k for k, v in mapping.items()}

        out = ""

        for digit in outputs[index]:
            out += output_map[frozenset(digit)]

        values.append(int(out, 10))

    return sum(values)

if __name__ == "__main__":

    ex1=pt1("./8/ex.txt")
    p1=pt1("./8/input.txt")
    ex2=pt2("./8/ex.txt")
    p2=pt2("./8/input.txt")

    print(f"ex: {ex1}")
    print(f"part1: {p1}")
    print(f"ex: {ex2}")
    print(f"part2: {p2}")
