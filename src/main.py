import networkx as nx
import numpy as np
import pagerank as pr
import utils
import random as rd


def main():
    n, t_edges = utils.patg_to_tedges("data/1_15_SMS.patg")
    min_t = min(t_edges, key=lambda x: x[2])[2]
    max_t = max(t_edges, key=lambda x: x[2])[2]
    st_edges = [str(e[0]) + ' ' + str(e[1]) + ' ' + str(e[2]) + ' ' + str(rd.randint(e[2], max_t+1000)) + '\n' for e in t_edges]
    print(len(st_edges))
    print(len(t_edges))
    with open("data/1_15_SMS.lstream", "w") as f:
        f.writelines(st_edges)
main()
