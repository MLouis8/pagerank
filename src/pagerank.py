import numpy as np
import networkx as nx
import math


def create_transition_and_dangling_matrices(
    graph: nx.DiGraph,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes the transition probability matrix and the dangling node vector
    from a directed weighted (on the edges) graph from networkx.
    """
    n = graph.number_of_nodes()
    h = np.zeros((n, n))
    a = np.zeros(n)
    edge_weights = nx.get_edge_attributes(graph, "weight", default=1)
    for u in graph:
        if list(graph.successors(u)) == []:
            a[u] = 1
        total_weight = sum([edge_weights[(u, v)] for v in graph.successors(u)])
        for v in graph.successors(u):
            h[u, v] = edge_weights[(u, v)] / total_weight
    return h, a


def static_pr_pwr(
    h_matrix: np.ndarray,
    a_vector: np.ndarray,
    alpha: float = 0.85,
    p_vector: np.ndarray | None = None,
    iter: int = 50,
    eps: float = 1e-5,
) -> np.ndarray:
    """
    Static PageRank implemented with the original power method.

    @parameters:
        h_matrix: hyperlink matrix (Markov matrix from original graph)
        a_vector: dangling node vector
        alpha:    probability of using h_matrix  / convergence ratio
        p_vector: personalization vector, if none then 1/n vector is taken
        iter:     number of iterations of the power method
        eps:      minimal convergence gap

    @returns:
        r: pagerank vector
    """
    n = len(h_matrix)
    if not isinstance(p_vector, np.ndarray):
        p_vector = np.ones((1, n)) * 1 / n
    r = p_vector
    for _ in range(iter):
        rr = alpha * r @ h_matrix + (alpha * r @ a_vector + 1 - alpha) * p_vector
        if np.linalg.norm(r - rr) < eps:
            return rr
        r = rr
    return rr


def temp_pr_tstamp_rdwalk(
    n: int,
    t_edges: list[tuple[int, int, int]],
    personalize: bool = True,
    p_vector: np.ndarray | None = None,
    t_end: float = math.inf,
    alpha: float = 0.85,
    beta: float = 1.0,
    save_steps: bool = False
) -> np.ndarray | list[np.ndarray]:
    """
    Temporal PageRank on timestamped edges.

    @parameters:
        n:           number of nodes in the graph
        t_edges:     list of timestamped edges
        personalize: if True then a normalization using p_vector is done
        p_vector:    personalization vector, if None given then out-degree vector is used (personalize needs to be True)
        t_end:       time limit (if None, every edge will be taken)
        alpha:       probability of folowwing the walk
        beta:        transition probability
        save_steps:  if True then each vector corresponding to an edge addition is saved and returned
    @returns:
        r: pagerank vector
    """
    t_edges.sort(key=lambda t: t[2])
    r, s = np.zeros(n), np.zeros(n)
    if save_steps:
        r_list = []
        prev_r = np.zeros(n)
    if personalize:
        h = np.zeros(n)
        for u, _, _ in t_edges:
            h[u] += 1
        h = h / len(t_edges)
        if isinstance(p_vector, np.ndarray):
            h = p_vector / (h / len(t_edges))
    for u, v, t in t_edges:
        if t > t_end:
            return r_list if save_steps else r
        if save_steps:
            r_list.append(prev_r)
            r_list[-1][u] = r_list[-1][u] + (1 - alpha) * h[u] if personalize else 1 - alpha
            s[u] = s[u] + (1 - alpha) * h[u] if personalize else 1 - alpha
            r_list[-1][v] += s[u] * alpha
        else:
            r[u] = r[u] + (1 - alpha) * h[u] if personalize else 1 - alpha
            s[u] = s[u] + (1 - alpha) * h[u] if personalize else 1 - alpha
            r[v] += s[u] * alpha
        if beta < 1:
            s[v] += s[u] * (1 - beta) * alpha
            s[u] *= beta
        else:
            s[v] += s[u] * alpha
            s[u] = 0
        if save_steps:
            prev_r = r_list[-1].copy()
    return r_list if save_steps else r


def temp_pr_linkstr_walk(
    n: int,
    t_edges: list,
    t_end: float,
    personalize: bool = True,
    p_vector: np.ndarray | None = None,
    alpha: float = 0.85,
    beta: float = 1.0,
) -> np.ndarray:
    """
    Temporal PageRank on link streams. The algorithm is based on the timestamped edges version.

    @parameters:
        n:           number of nodes in the graph
        t_edges:     list of temporal edges
        t_end:       time limit
        personalize: if True then a normalization using p_vector is done
        p_vector:    personalization vector, if None given then out-degree vector is used (personalize needs to be True)
        alpha:       probability of folowwing the walk
        beta:        transition probability

    @returns:
        r: pagerank vector
    """
    t_edges.sort(key=lambda t: t[2])
    valid_t_edges = filter(lambda e: e[3] < t_end, t_edges)
    r, s = np.zeros(n), np.zeros(n)
    if personalize:
        h = np.zeros(n)
        for u, _, _, _ in t_edges:
            h[u] += 1
        h = h / len(t_edges)
        if isinstance(p_vector, np.ndarray):
            h = p_vector / (h / len(t_edges))
    for u, v, _, _ in valid_t_edges:
        r[u] += (1 - alpha) * h[u] if personalize else 1 - alpha
        s[u] += (1 - alpha) * h[u] if personalize else 1 - alpha
        r[v] += s[u] * alpha
        if beta < 1:
            s[v] += s[u] * (1 - beta) * alpha
            s[u] *= beta
        else:
            s[v] += s[u] * alpha
            s[u] = 0
    return r


def temp_pr_linkstr(
    n: int,
    t_edges: list,
    t_end: float = math.inf,
    alpha: float = 0.85,
    p_vector: np.ndarray | None = None,
    iter: int = 50,
    eps: float = 1e-5,
) -> np.ndarray:
    """
    Temporal PageRank like measure. It works like the original pagerank but adds temporal informations.

    @parameters:
        n:           number of nodes
        t_edges:     list of temporal edges
        t_end:       time limit (if None, every edge is used)
        alpha:       probability of using h_matrix  / convergence ratio
        p_vector:    personalization vector, if none then 1/n vector is taken
        iter:        number of iterations of the power method
        eps:         minimal convergence gap

    @returns:
        r: pagerank vector
    """
    valid_t_edges, flag = [], True
    for edge in t_edges:
        if edge[3] < t_end:
            valid_t_edges.append(edge)
            falg = False
    if flag:
        return np.zeros(n)
    time_length = min(max(valid_t_edges, key=lambda x: x[1]), t_end) - min(
        valid_t_edges, key=lambda x: x[0]
    )
    digraph_edges = [
        (e[0], e[1], {"weight": (e[1] - e[0]) / time_length}) for e in valid_t_edges
    ]
    G = nx.DiGraph()
    G.add_edges_from(digraph_edges)
    h, a = create_transition_and_dangling_matrices(G)
    return static_pr_pwr(h, a, alpha, p_vector, iter, eps)
