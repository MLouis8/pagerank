import networkx as nx
import numpy as np


def lstream_to_tedges(fpath: str) -> tuple[int, list[tuple[int, int, int, int]]]:
    with open(fpath, "r") as lstream_file:
        n = int(lstream_file.readline(1))
        lines = lstream_file.readlines()[1:]
    f = lambda l: (int(l[0]), int(l[1]), int(l[2]), int(l[3]))
    pre_tedges = [f(line.split(" ")) for line in lines]
    min_node = pre_tedges[0][0]
    for edge in pre_tedges:
        if edge[0] < min_node:
            min_node = edge[0]
        if edge[1] < min_node:
            min_node = edge[1]
    tedges = [(e[0] - min_node, e[1] - min_node, e[2], e[3]) for e in pre_tedges]
    return n, tedges


def patg_to_tedges(fpath: str) -> tuple[int, list[tuple[int, int, int]]]:
    with open(fpath, "r") as patg_file:
        n = int(patg_file.readline(1))
        lines = patg_file.readlines()[1:]
    f = lambda l: (int(l[0]), int(l[1]), int(l[2]))
    pre_tedges = [f(line.split(" ")) for line in lines]
    min_node = pre_tedges[0][0]
    for edge in pre_tedges:
        if edge[0] < min_node:
            min_node = edge[0]
        if edge[1] < min_node:
            min_node = edge[1]
    tedges = [(e[0] - min_node, e[1] - min_node, e[2]) for e in pre_tedges]
    return n, tedges


def pagerank_ranking(r: np.ndarray) -> list:
    return sorted(range(len(r)), key=lambda k: r[k], reverse=True)


def digraph_from_edges(t_edges: list) -> nx.digraph:
    G = nx.Digraph()
    if len(t_edges[0]) == 3:
        digraph_edges = [(e[0], e[1], {"weight": e[2]}) for e in t_edges]
    elif len(t_edges[0]) == 4:
        time_length = max(t_edges, key=lambda x: x[1]) - min(
            t_edges, key=lambda x: x[0]
        )
        digraph_edges = [
            (e[0], e[1], {"weight": (e[1] - e[0]) / time_length}) for e in t_edges
        ]
    G.add_edges_from([digraph_edges])
    return G
