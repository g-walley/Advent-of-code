from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from parse import parse
from networkx import DiGraph
import networkx as nx
import pydotplus as pdp
import re


def parse_input(raw_input: Path) -> DiGraph:
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
    return g


def back_propagation(g: DiGraph, root: str) -> DiGraph:
    leaves_in_parent_vals = set()
    # print([(leaf, g.nodes[leaf]["val"]) for leaf in leaves])
    while list(g.nodes()) != [root]:

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
    return g

def forward_propagation(g: DiGraph, root: str, root_val: int):

    leaves_in_parent_vals = set()
    leaves = {
        node
        for node in g.nodes()
        if not g.succ[node] and node not in leaves_in_parent_vals
    }
    while leaves != {"humn"}:

        while leaves:
            leaf = leaves.pop()
            if leaf == "humn":
                continue
            try:
                val = int(g.nodes[leaf]["val"])
            except KeyError:
                ...
            pred_node = list(g.pred[leaf])[0]

            c_vals: Dict[str, int] = g.nodes[pred_node].get("c_vals", {})
            c_vals[leaf] = val
            g.nodes[pred_node]["c_vals"] = c_vals
            leaves_in_parent_vals.add(leaf)

        nodes_to_remove = []
        for node in list(g.nodes()):
            d: Dict[str,Any] = g.nodes[node]
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

        leaves = {
            node
            for node in g.nodes()
            if not g.succ[node] and node not in leaves_in_parent_vals
        }

    # from root
    # set val of root
    g.nodes[root]["val"] = root_val
    n = root
    # get successors of root:
    dg = generate_dot_graph(g)
    dg.write("2022/day21/day21pt2_test.pdf", format="pdf")
    while n != "humn":
        s = list(g.succ[n])
        try:
            child_vals = g.nodes[n]["c_vals"]
        except KeyError:
            ...
        if s[0] in child_vals:
            child = s[1]
            mod_val = child_vals[s[0]]
        elif s[1] in child_vals:
            child = s[0]
            mod_val = child_vals[s[1]]

        # print(f"{child}, {mod_val}")
        # ensuring ordering, use inverse of op to calculate val for node that isnt in the c_vals list
        if g.nodes[n]["op"] == "+":
            v = g.nodes[n]["val"] - mod_val
        elif g.nodes[n]["op"] == "-":
            if child == s[0]:
                v = mod_val + g.nodes[n]["val"]
            elif child == s[1]:
                v = mod_val - g.nodes[n]["val"]
        elif g.nodes[n]["op"] == "/":
            if child == s[0]:
                v = mod_val * g.nodes[n]["val"]
            elif child == s[1]:
                v = mod_val / g.nodes[n]["val"]
        elif g.nodes[n]["op"] == "*":
            v = g.nodes[n]["val"] / mod_val
        else:
            assert False, "Operation invalid."
        g.nodes[child]["val"] =v
        n = child
    return g.nodes["humn"]["val"]


def pt1(raw_input: Path):
    """part 1"""
    g = parse_input(raw_input)

    g = back_propagation(g, "root")

    return g.nodes["root"]["val"]


def split_graph(g: DiGraph, roots: List[str]) -> Tuple[DiGraph, DiGraph]:


    def get_successors(nodes: Set, checked: Set):
        pre = deepcopy(nodes)
        n = list(nodes)
        for node in n:
            if node not in checked:
                for succ in g.succ[node]:
                    nodes.add(succ)
                checked.add(node)

        if nodes == pre:
            return nodes
        else:
            return get_successors(nodes, checked)

    a_nodes = get_successors({roots[0]}, set())
    b_nodes = get_successors({roots[1]}, set())

    g_a = g.subgraph(a_nodes)
    g_b = g.subgraph(b_nodes)
    return (DiGraph(g_a), DiGraph(g_b))


def pt2(raw_input: Path):
    """part 2"""
    g = parse_input(raw_input)
    dg: pdp.Dot = generate_dot_graph(g)
    dg.write("2022/day21/day21pt2.svg", format="svg")
    roots = list(g.succ["root"])
    a, b = split_graph(g, roots)

    if "humn" in a.nodes():
        b = back_propagation(b, roots[1])
        return forward_propagation(a, roots[0], b.nodes[roots[1]]["val"])
        # forward prop a
    elif "humn" in b.nodes():
        a = back_propagation(a, roots[0])
        return forward_propagation(b, roots[1], a.nodes[roots[0]]["val"])
        # forward prop b


def generate_dot_graph(graph: DiGraph):
    node_list = list(graph.nodes())
    edge_list = list(graph.edges())
    graph = pdp.Dot(graph_type="digraph", rankdir="LR")

    for edge in edge_list:
        graph.add_edge(
            pdp.Edge(
                edge[0],
                edge[1],
                label="",
                labelfontcolor="#009933",
                fontsize="10.0",
                color="black",
            )
        )
    for node in node_list:
        fill_node_colour = "lightgrey"
        graph.add_node(
            pdp.Node(name=node, label=node, style="filled", fillcolor=fill_node_colour)
        )
    return graph
