import numpy as np
import networkx as nx
import math

def create_transition_and_dangling_matrices(graph: nx.DiGraph):
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
            h[u-1, v-1] = edge_weights[(u, v)] / total_weight
    return h, a

def static_pr_pwr(h_matrix, a_vector, alpha=0.85, p_vector=None, iter=50, eps=1e-5):
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
        p_vector = np.ones((1, n)) * 1/n
    r = p_vector
    for _ in range(iter):
        rr = alpha * r @ h_matrix + (alpha * r @ a_vector + 1 - alpha) * p_vector
        if np.linalg.norm(r - rr) < eps:
            return rr
        r = rr
    return rr



def temp_pr_tstamp_rdwalk(n: int, t_edges: list[tuple[int,int,int]], personalize=True, p_vector=None, t_end=math.inf, alpha=0.85, beta=1):
    """
    Temporal PageRank on timestamped edges.

    @parameters:
        n:           number of nodes in the graph
        t_edges:     list of timestamped edges, ordered by timestamp
        personalize: if True then a normalization using p_vector is done
        p_vector:    personalization vector, if None given then out-degree vector is used (personalize needs to be True)
        t_end:       last timestamp accepted in the walks (if None, every edge will be taken)
        alpha:       probability of folowwing the walk
        beta:        transition probability
    
    @returns:
        r: pagerank vector
    """
    t_edges.sort(key=lambda t: t[2])
    r, s = np.zeros(n), np.zeros(n)
    if personalize:
        h = np.zeros(n)
        for (u, _, _) in t_edges:
            h[u] += 1
        h = h / len(t_edges)
        if isinstance(p_vector, np.ndarray):
            h = p_vector / (h / len(t_edges))
    for (u, v, t) in t_edges:
        if t > t_end:
            return r
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

def temp_pr_linkstr_walk():
    """
    Temporal PageRank on link streams. The algorithm is based on the timestamped edges version, but runs in reverse.
    This way it ensures that paths exist even with deletions.
    """
    pass


def temp_pr_linkstr_static(h_matrix, a_vector, alpha=0.85, p_vector=None, iter=50, eps=1e-5):
    """
    Temporal PageRank like measure on link streams. Transform a temporal network into a static one,
    using link durations to weight each edge.
    
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
        p_vector = np.ones((1, n)) * 1/n
    r = p_vector
    for _ in range(iter):
        rr = alpha * r @ h_matrix + (alpha * r @ a_vector + 1 - alpha) * p_vector
        if np.linalg.norm(r - rr) < eps:
            return rr
        r = rr
    return rr