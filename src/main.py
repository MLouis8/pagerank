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
    temp_pr = pr.temp_pr_tstamp_rdwalk(n, t_edges, save_steps=True)
    print("pageranks computed...")
    plot.convergence_plot("convergence.jpg", static_pr, temp_pr)

def pr_comparison():
    n, t_edges = utils.patg_to_tedges("data/1_15_SMS.patg")
    G = utils.digraph_from_edges(t_edges, False)
    print("graphs loaded...")
    h, a = pr.create_transition_and_dangling_matrices(G)
    static_pr = pr.static_pr_pwr(h, a)
    print("static pr computed...")

def compare_original_pr():
    n, t_edges = utils.patg_to_tedges("data/graph1.patg")
    G = utils.digraph_from_edges(t_edges, False)
    h, a = pr.create_transition_and_dangling_matrices(G)
    p = [len(list(G.successors(u))) / len(G.edges)for u in G.nodes]
    p_vector = np.array([p])
    static_pr = pr.static_pr_pwr(h, a, p_vector=p_vector)[0]
    p_dict = {i: p[i] for i in range(n)}
    pagerank = nx.pagerank(G, personalization=p_dict, weight='weight')
    print(static_pr)
    print(pagerank)
    print(pearsonr(static_pr, list(pagerank.values())).statistic)

def main():
    compare_original_pr()
main()
