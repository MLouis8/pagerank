import matplotlib.pyplot as plt
from utils import pagerank_ranking
import numpy as np
from scipy.stats import pearsonr

def convergence_plot(fname: str, static_pr: np.ndarray, temp_pr: list, delta=1):
    static_rank = pagerank_ranking(static_pr)
    ax = plt.subplot()
    k = len(temp_pr)
    x_temp, y_temp = np.arange(0, k, delta), np.zeros(k//delta)
    for j in range(0, k, delta):
        y_temp[j//delta] = pearsonr(temp_pr[j], static_pr).statistic
    ax.plot(x_temp, y_temp, label="temporal pagerank")
    ax.set_xlabel("nb of temporal edges")
    ax.set_ylabel("correlation coeff")
    ax.set_ylim(0., 1.1)
    ax.legend()
    ax.set_title("Convergence of temporal pagerank to static pagerank")
    plt.savefig(fname)

def pagerank_evolution_plot(fname: str, static_pr: np.ndarray, temp_prs: list, labels: list):
    static_rank = pagerank_ranking(static_pr)
    ax = plt.subplot()
    first = np.argmin(np.array(static_rank))
    for i, temp_pr in enumerate(temp_prs):
        x_temp, y_temp = np.arange(i), np.zeros(i)
        for j in range(len(temp_pr)):
            y_temp[j] = temp_pr[j][first]
        ax.plot(x_temp, y_temp, label=labels[i])
    ax.legend()
    ax.set_title("Temporal Pagerank rankings for node with biggest static pagerank")
    ax.set_xlabel("time")
    ax.set_ylabel("rank")
    plt.savefig(fname)