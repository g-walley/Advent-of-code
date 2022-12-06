from typing import Dict, List, Set, Tuple
import numpy as np
from pathlib import Path
from collections import Counter


def deal_with_dead_end(adj_dict, dead_end, i_paths):
    for dst_nodes in adj_dict.values():
        if dead_end in dst_nodes:
            dst_nodes.remove(dead_end)

    for path in i_paths.copy():
        if dead_end in path:
            i_paths.remove(path)

def dict_factory(lines):
    adj_dict: Dict[str, Set]= {}
    for line in lines:
        src, dst = line.split("-")
        if dst == "start" or src == "end":
            dst, src = (src, dst)

        try:
            adj_dict[src]
        except KeyError:
            adj_dict[src] = set()
        finally:
            adj_dict[src].add(dst)

        if src != "start" and dst != "end":
            try:
                adj_dict[dst]
            except KeyError:
                adj_dict[dst] = set()
            finally:
                adj_dict[dst].add(src)

    return adj_dict

def pt1(lines: List[str]) -> np.int64:
    """Part 1"""

    adj_dict = dict_factory(lines)

    i_paths = {("start",)}  # incomplete paths
    c_paths = set()  # complete paths
    while i_paths:
        for path in i_paths.copy():
            i_paths.remove(path)

            try:
                dst_nodes: Set[str] = adj_dict[path[-1]]
                for node in dst_nodes:
                    if node == "end":
                        c_paths.add(path + (node,))
                    elif ((node.islower() and node not in path) or
                        node.isupper()):
                        i_paths.add(path + (node,))
            except KeyError:
                dst_to_delete = path[-1]
                deal_with_dead_end(
                    adj_dict=adj_dict,
                    dead_end=dst_to_delete,
                    i_paths=i_paths,
                )

    return len(c_paths)


def repeats(path: Tuple[str])-> str:
    counts = Counter(list(path))
    for node, count in counts.items():
        if node.islower() and count > 1:
            return node
    return None

def pt2(lines) -> np.int64:
    """Part 2"""

    adj_dict = dict_factory(lines)

    i_paths = {("start",)}  # incomplete paths

    c_paths = set()  # complete paths
    while i_paths:
        for path in i_paths.copy():
            i_paths.remove(path)

            try:
                dst_nodes: Set[str] = adj_dict[path[-1]]
                for node in dst_nodes:
                    repeating_char = repeats(path)
                    if node == "end":
                        c_paths.add(path + (node,))
                    elif (repeating_char is None or node.isupper()):
                        i_paths.add(path + (node,))
                    elif(
                        repeating_char is not None and
                        node.islower() and node not in path):
                        i_paths.add(path + (node,))

            except KeyError:
                dst_to_delete = path[-1]
                deal_with_dead_end(
                    adj_dict=adj_dict,
                    dead_end=dst_to_delete,
                    i_paths=i_paths,
                )

    return len(c_paths)


if __name__ == "__main__":
    ex1_in = Path("./12/ex1.txt").read_text(encoding="utf-8").splitlines()
    ex2_in = Path("./12/ex2.txt").read_text(encoding="utf-8").splitlines()
    ex3_in = Path("./12/ex3.txt").read_text(encoding="utf-8").splitlines()
    my_in = Path("./12/input.txt").read_text(encoding="utf-8").splitlines()
    ex1_1 = pt1(ex1_in)
    print(f"ex1_1: {ex1_1}")
    ex2_1 = pt1(ex2_in)
    print(f"ex1_2: {ex2_1}")
    ex3_1 = pt1(ex3_in)
    print(f"ex1_3: {ex3_1}")
    p1 = pt1(my_in)
    print(f"part1: {p1}")
    ex1_2 = pt2(ex1_in)
    print(f"ex2_1: {ex1_2}")
    ex2_2 = pt2(ex2_in)
    print(f"ex2_2: {ex2_2}")
    ex3_2 = pt2(ex3_in)
    print(f"ex2_3: {ex3_2}")
    p2 = pt2(my_in)
    print(f"part2: {p2}")

