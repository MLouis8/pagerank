import networkx as nx
import numpy as np
import pagerank as pr
import random as rd
import utils
import plot
from scipy.stats import pearsonr

def convergence_experiment():
    n, t_edges = utils.patg_to_tedges("data/1_01_hypertext.patg")
    G = utils.digraph_from_edges(t_edges, False)
    h, a = pr.create_transition_and_dangling_matrices(G)
    p = [len(list(G.successors(u))) / len(G.edges)for u in G.nodes]
    p_vector = np.array([p])
    static_pr = pr.static_pr_pwr(h, a, p_vector=p_vector)[0]
    print("static pr computed...")
    t_edges_extended = utils.extend_tedgelist(t_edges, 100000)
    
    temp_pr = pr.temp_pr_tstamp_rdwalk(n, t_edges_extended, save_steps=True)
    print("pageranks computed...")
    plot.convergence_plot("convergence.jpg", static_pr, temp_pr, 100)

def pr_comparison():
    n, t_edges = utils.patg_to_tedges("data/graph1.patg")
    G = utils.digraph_from_edges(t_edges, False)
    print("graphs loaded...")
    h, a = pr.create_transition_and_dangling_matrices(G)
    static_pr = pr.static_pr_pwr(h, a)[0]
    print("static pr computed...")
    temp_pr = pr.temp_pr_tstamp_rdwalk(n, t_edges, save_steps=True)
    max_time = max(t_edges)
    for t in range(max_time):
        links_pr1 = pr.temp_pr_linkstr_walk(n, t_edges, t_end=t)
        links_pr2 = pr.temp_pr_linkstr()

def compare_original_pr():
    n, t_edges = utils.patg_to_tedges("data/graph1.patg")
    G = utils.digraph_from_edges(t_edges, False)
    h, a = pr.create_transition_and_dangling_matrices(G)
    p = [len(list(G.successors(u))) / len(G.edges)for u in G.nodes]
    p_vector = np.array([p])
    static_pr = pr.static_pr_pwr(h, a, p_vector=p_vector)[0]
    p_dict = {i: p[i] for i in range(n)}
    pagerank = nx.pagerank(G, alpha=0.85, personalization=p_dict, weight='weight')
    pr_vector = [pagerank[i] for i in range(len(static_pr))]
    print(pearsonr(static_pr, pr_vector).statistic)

def main():
    pr_comparison()
main()
