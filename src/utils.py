import networkx as nx
import numpy as np
import random as rd


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
        n = int(patg_file.readline())
        lines = patg_file.readlines()
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


def digraph_from_edges(t_edges: list, time_weight: bool) -> nx.digraph:
    G = nx.DiGraph()
    if time_weight:
        if len(t_edges[0]) == 3:
            digraph_edges = [(e[0], e[1], {"weight": e[2]}) for e in t_edges]
        elif len(t_edges[0]) == 4:
            time_length = max(t_edges, key=lambda x: x[1]) - min(
                t_edges, key=lambda x: x[0]
            )
            digraph_edges = [
                (e[0], e[1], {"weight": (e[1] - e[0]) / time_length}) for e in t_edges
            ]
    else:
        digraph_edges = [(e[0], e[1]) for e in t_edges]
        digraph_edges = list(set(digraph_edges)) 
    G.add_edges_from(digraph_edges)
    return G

def extend_tedgelist(t_edges: list, n: int) -> list:
    min_t = min(t_edges, key=lambda x: x[2])
    max_t = max(t_edges, key=lambda x: x[2])
    edges = list(set([(e[0], e[1]) for e in t_edges]))
    w = [1/len(edges) for edge in edges]
    new_edges = rd.choices(edges, k=n, weights=w)
    new_tedges = [(e[0], e[1], i) for i, e in enumerate(new_edges)]
    return new_tedges

def patg_to_lstream(fname: str, new_fname: str):
    t_edges = patg_to_tedges(fname)
    max_t = max(t_edges, key=lambda x: x[2])[2]
    st_edges = [str(e[0]) + ' ' + str(e[1]) + ' ' + str(e[2]) + ' ' + str(rd.randint(e[2], max_t+1000)) + '\n' for e in t_edges]
    print(len(st_edges))
    print(len(t_edges))
    with open(new_fname, "w") as f:
        f.writelines(st_edges)