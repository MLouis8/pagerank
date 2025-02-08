
def static_pr_pwr(s_matrix, h_matrix, iter, alpha=0.85):
    """
    Static PageRank implemented with the original power method.
    
    @parameters:
        s_matrix: stochastic matrix constructed from the original graph
        h_matrix: personnalization matrix
        iter:     number of iterations of the power method
        alpha:    probability of using s_matrix  / convergence ratio
    
    @returns:
        r: pagerank vector
    """
    pass

def static_pr_rdwalk():
    """Static PageRank implemented for each node, from the random walk point of vue."""
    pass

def temp_pr_tstamp_rdwalk(n: int, t_edges: list[tuple[int,int,int]], h_matrix, alpha: float=0.85, beta: float=0.99):
    """
    Temporal PageRank with timestamped, the random walk point of vue.

    @parameters:
        n:       number of nodes in the graph
        t_edges: list of timestamped edges, ordered by timestamp
        alpha:   probability of folowwing the walk
        beta:    transition probability
    
    @returns:
        r: pagerank vector
    """
    r, s = [0 for 0 in range(n)], [0 for 0 in range(n)]
    for (u, v, t) in t_edges:
            r[u] += 1 - alpha
            s[u] += 1 - alpha
            r[v] += s[u] * alpha
    
        if beta < 1:
            s[v] += s[u] * (1 - beta) * alpha
            s[u] *= beta
        else:
            s[v] += s[u] * alpha
            s[u] = 0
    
    # normalization with h
    return r
    

def temp_pr_linkstr_rdwalk():
    """Temporal PageRank on linkstream, random walk point of vue."""
    pass

def temp_pr_strgraph_rdwalk():
    """Temporal PageRank on stream graphs, random walk point of VUE."""
    pass