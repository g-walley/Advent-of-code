from dataclasses import dataclass
from pathlib import Path
from typing import Tuple
from networkx import DiGraph

@dataclass
class Mapping:
    src: int
    dst: int
    rng: int

def pt1(raw_input: Path):
    """part 1"""
    lines = raw_input.read_text().split("\n\n")

    line_dict = {
        line.split(":")[0].strip(): line.split(":")[1].strip().splitlines()
        for line in lines
    }
    schematic = DiGraph(multigraph=False)
    seeds = [int(num) for num in line_dict["seeds"][0].split()]

    mappings = list(line_dict)
    mappings.remove("seeds")

    for key in set(mappings):
        parent, child = tuple(key.strip(" map").split("-to-"))

        # if parent not in schematic.nodes():
        #     schematic.add_node(parent)
        # if child not in schematic.nodes():
        #     schematic.add_node(child)
        mappings = []
        for number_range in line_dict[key]:
            to_min, from_min, span = tuple(map(int, number_range.split()))
            schematic.add_edge(parent, child, rule=Mapping(from_min, to_min, span))

    locations = []
    adjacency = schematic.adjacency()
    node_name = "seed"



def pt2(raw_input: Path):
    """part 2"""
