import networkx as nx
import numpy as np
import pagerank as pr
import random as rd
import utils
import plot



def main():
    graph1_nx = nx.DiGraph(
        [(1, 2), (3, 5), (5, 6), (1, 3), (4, 5), (6, 4), (3, 1), (4, 6), (3, 2), (5, 4)]
    )
    h, a = pr.create_transition_and_dangling_matrices(graph1_nx)
    p = np.array([[2/10, 0, 3/10, 2/10, 2/10, 1/10]])
    static_pr = pr.static_pr_pwr(h, a, p_vector=p)[0]
    print(static_pr)

    n, t_edges = utils.patg_to_tedges("data/graph1.patg")
    t_edges_extended = utils.extend_tedgelist(t_edges, 100)
    temp_pr = []
    for k in range(1, 100):
        temp_pr.append(pr.temp_pr_tstamp_rdwalk(n, t_edges_extended[:k]))
    plot.convergence_plot("convergence.jpg", static_pr, [temp_pr], ["temporal"])
    print(static_pr)
    print(temp_pr)
    print("ranks", utils.pagerank_ranking(static_pr))
    for temp in temp_pr:
        print(utils.pagerank_ranking(temp))
main()
