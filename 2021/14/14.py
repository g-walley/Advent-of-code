from collections import defaultdict
from typing import DefaultDict, Dict, List, Tuple
from pathlib import Path
import numpy as np
from time import time
from functools import wraps

def timing(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start = time()
        result = method(*args, **kwargs)
        end = time()
        print(f"Elapsed time: {end-start}")
        return result
    return wrapper


def create_mapping(in_file: str) -> Tuple[str, Dict[str, str]]:
    lines = Path(in_file).read_text(encoding="utf-8").splitlines()
    char_map = {}
    for line_i, line in enumerate(lines):
        if line_i == 0:
            template = line.strip()
        elif line.strip() == "":
            continue
        else:
            char_map[line.split(" -> ")[0]] = line.split(" -> ")[1]

    return (template, char_map)


def create_child_mapping(orig_mapping: Dict[str, str]) -> Dict[str, List[str]]:
    child_map = {}
    for key, insert in orig_mapping.items():
        children = [
            key[0] + insert,
            insert + key[1],
        ]
        child_map[key] = children

    return child_map

def pt1(polymer, mapping, num_steps) -> np.int64:
    """Part 1"""
    unique_chars = set(polymer)
    counts = DefaultDict(int)
    for cha in unique_chars:
        counts[cha] += 1

    for step in range(num_steps):
        new_poly = ""
        for idx, cha in enumerate(polymer):
            if idx == len(polymer) - 1:
                new_poly += cha
            else:
                key = cha + polymer[idx + 1]
                new_cha = mapping[key]
                new_poly += cha + new_cha
                counts[new_cha] += 1
        polymer = new_poly
        print(f"Step {step}: {len(polymer)}")

    return max(counts.values()) - min(counts.values())

@timing
def pt2(polymer, char_map: Dict[str, str], num_steps) -> np.int64:
    child_map = create_child_mapping(char_map)
    pair_counts = defaultdict(int)
    for idx in range(len(polymer) - 1):
        pair_counts[polymer[idx] + polymer[idx + 1]] += 1

    char_counts = defaultdict(int)
    for char in polymer:
        char_counts[char] += 1

    for _ in range(num_steps):
        new_pair_counts = defaultdict(int)
        for pair in pair_counts.copy():
            count = pair_counts.pop(pair)

            for child in child_map[pair]:
                new_pair_counts[child] += count
                char = child[0]

            char_counts[char] += count
        pair_counts = new_pair_counts

    return max(char_counts.values()) - min(char_counts.values())


if __name__ == "__main__":
    template, mapping = create_mapping("./14/example.txt")
    ex1=pt2(template, mapping, 10)
    ex2=pt2(template, mapping, 40)
    template, mapping = create_mapping("./14/input.txt")
    p1=pt2(template, mapping, 10)
    p2=pt2(template, mapping, 40)

    print(f"ex1: {ex1}")
    print(f"ex2: {ex2}")
    print(f"part1: {p1}")
    print(f"part2: {p2}")
