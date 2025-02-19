import matplotlib.pyplot as plt
from utils import pagerank_ranking
import numpy as np

def convergence_plot(fname: str, static_pr: ndarray, temp_prs: list, labels: list):
    static_rank = pagerank_ranking(static_pr)
    for i, temp_pr in enumerate(temp_prs):
        k = len(temp_pr)
        flag, cv_bar = False, 0
        x_temp, y_temp = np.arange(k), np.zeros(k)
        for j in range(k):
            y_temp[j] = np.linalg.norm(static_pr - temp_pr[j])
            current_rank = pagerank_ranking(temp_pr[j])
            if flag and current_rank == static_pr:
                flag = True
                cv_bar = j
        plt.plot(x_temp, y_temp, label=labels[i])
        plt.axvline(x=cv_bar, label=labels[i])
    plt.legend()
    plt.savefig(fname)

def pagerank_evolution_plot(fname: str, static_pr: ndarray, temp_prs: list, labels: list):
    static_rank = pagerank_ranking(static_pr)
    first = np.argmin(np.array(static_rank))
    for i, temp_pr in enumerate(temp_prs):
        x_temp, y_temp = np.arange(k), np.zeros(k)
        for j in range(len(temp_pr)):
            y_temp[j] = temp_pr[j][first]
        plt.plot(x_temp, y_temp, label=labels[i])
    plt.legend()
    plt.savefig(fname)
    