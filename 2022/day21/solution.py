from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List
from parse import parse
from networkx import DiGraph
import re


def pt1(raw_input: Path):
    """part 1"""
    monkey_list = raw_input.read_text(encoding="utf-8").splitlines()

    monkey_troop = {}
    for monkey in monkey_list:
        p = parse("{name}: {the_rest}", monkey)
        monkey_troop[p["name"]] = p["the_rest"]

    # print(monkey_troop)
    r_c = re.compile(
        r"^(?P<num>[\d]+)?$|^(?P<c1>[a-z]{4}) (?P<op>[+\-*/]) (?P<c2>[a-z]{4})$"
    )

    g = DiGraph()
    leaves_w_child_to_add = {"root"}
    while monkey_troop:
        while leaves_w_child_to_add:
            leaf = leaves_w_child_to_add.pop()
            m = re.search(r_c, monkey_troop.pop(leaf))
            if m["num"]:
                g.nodes[leaf]["val"] = m["num"]
            elif m["op"]:
                g.add_node(leaf, op=m["op"])
                kids = [m["c1"], m["c2"]]
                g.add_nodes_from(kids)
                g.add_edges_from(zip([leaf] * 2, kids))
            else:
                assert False, "Regex returned unexpected result!"

        leaves_w_child_to_add = {
            node
            for node in g.nodes()
            if not g.succ[node] and not g.nodes[node].get("val", None)
        }

    leaves_in_parent_vals = set()
    # print([(leaf, g.nodes[leaf]["val"]) for leaf in leaves])
    while list(g.nodes()) != ["root"]:

        leaves = {
            node
            for node in g.nodes()
            if not g.succ[node] and node not in leaves_in_parent_vals
        }
        while leaves:
            leaf = leaves.pop()
            val = int(g.nodes[leaf]["val"])
            pred_node = list(g.pred[leaf])[0]

            c_vals: Dict[str, int] = g.nodes[pred_node].get("c_vals", {})
            c_vals[leaf] = val
            g.nodes[pred_node]["c_vals"] = c_vals
            leaves_in_parent_vals.add(leaf)

            # print("-----")
            # for node, val in g.nodes().items():
            #     print(f"{node}: {val}")

        nodes_to_remove = []
        for node in list(g.nodes()):
            d: Dict[str, Any] = g.nodes[node]
            if len(d.get("c_vals", [])) == 2:
                kids = list(g.succ[node])

                if d["op"] == "+":
                    d["val"] = d["c_vals"][kids[0]] + d["c_vals"][kids[1]]
                elif d["op"] == "/":
                    d["val"] = d["c_vals"][kids[0]] / d["c_vals"][kids[1]]
                elif d["op"] == "-":
                    d["val"] = d["c_vals"][kids[0]] - d["c_vals"][kids[1]]
                elif d["op"] == "*":
                    d["val"] = d["c_vals"][kids[0]] * d["c_vals"][kids[1]]

                nodes_to_remove.extend(kids)

                d.pop("c_vals")
                d.pop("op")

        g.remove_nodes_from(nodes_to_remove)

    return g.nodes["root"]["val"]

def pt2(raw_input: Path):
    """part 2"""
