import networkx as nx
import numpy as np
import pagerank as pr
import utils


def main():
    print("static PageRank")
    graph1_nx = nx.DiGraph(
        [(1, 2), (3, 5), (5, 6), (1, 3), (4, 5), (6, 4), (3, 1), (4, 6), (3, 2), (5, 4)]
    )
    h, a = pr.create_transition_and_dangling_matrices(graph1_nx)
    # p = np.array([[2/10, 0, 3/10, 2/10, 2/10, 1/10]])
    r = pr.static_pr_pwr(h, a)
    print("first graph")
    print("pagerank vector: ", r)
    print("pagerank ranking: ", utils.pagerank_ranking(r[0]))

    # graph2_nx = nx.DiGraph([(1, 3), (2, 1), (2, 5), (2, 8), (3, 1), (3, 2), (3, 7), (4, 5), (5, 1), (6, 5), (7, 1), (8, 5)])
    # h, a = pr.create_transition_and_dangling_matrices(graph2_nx)
    # p = np.array([[1/12, 3/12, 3/12, 1/12, 1/12, 1/12, 1/12, 1/12]])
    # r = pr.static_pr_pwr(h, a, p_vector=p)
    # print("second graph")
    # print("pagerank vector: ", r)
    # print("pagerank ranking: ", utils.pagerank_ranking(r[0]))

    # print("Temporal PageRank")
    # n, t_edges_1 = utils.patg_to_tedges("data/graph1.patg")
    # r = pr.temp_pr_tstamp_rdwalk(n, t_edges_1)
    # print("pagerank vector: ", r)
    # print("pagerank ranking: ", utils.pagerank_ranking(r))

    # n, t_edges_2 = utils.patg_to_tedges("data/graph2_a.patg")
    # print("second graph, timestamp A")
    # for t in range(1, 13):
    #     r = pr.temp_pr_tstamp_rdwalk(n, t_edges_2, t_end=t, personalize=True)
    #     print("pagerank ranking: ", utils.pagerank_ranking(r))
    # n, t_edges_2 = utils.patg_to_tedges("data/graph2_b.patg")
    # print("second graph, timestamp B")
    # for t in range(1, 13):
    #     r = pr.temp_pr_tstamp_rdwalk(n, t_edges_2, t_end=t, personalize=True)
    #     print("pagerank ranking: ", utils.pagerank_ranking(r))


main()
