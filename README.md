# Temporal PageRank

The objective of this project is to explore the pagerank algorithm and its temporal versions.

## Content

The algorithms are implemented [here](./src/pagerank.py)

### Original Pagerank ```static_pr_pwr```
The basic pagerank [[1]](#1) with the power method is implemented as a reference algorithm to test convergence of the other algorithms when all time features are equal.
It computes the pagerank vector $\pi^k$ at $k$-th iteration such that:

$$\pi^{k+1} = \alpha \pi^k \cdot H + (\alpha \pi^k \cdot a + 1-\alpha) p$$

with $\pi^0$ an arbitrary vector, $\alpha$ the jumping probability, $a$ the dangling node vector, $H$ the stochastic matrix of transitions in the graph and $p$ the personalization vector.

**Complexity:** $O(n^2)$ but with sparse hyperlink matrices it is nearly linear.

### Temporal Pagerank ```temp_pr_tstamp_rdwalk```
It's the algorithm from [[2]](#2). It works on temporal edges where only the starting time is given, we call this edges *timestamped edges*.
Here, the random walk point of vue is taken and the temporal pagerank for a node $u$ at time $t$ is:

$$r(u, t) = \sum_{v \in V} \sum_{k=0}^{t} (1-\alpha)\alpha^k \sum_{z\in Z(v, u | t) \wedge |z| = k} Pr[z\ |\ t]$$

Knowing that:
- $Z(v, u|t)$ is
- $Pr[z|t]$ is

**Complexity:** The implementation is linear in the number of edges with one or two pass (whether a personalization vector is used or not). It takes temporal edges one by one, allowing the user to have the pagerank vector a each time step.

### Temporal Pagerank on link streams

#### Random walk based version ```temp_pr_linkstr_walk```
On this algorithm, the edges have now also an ending time [[3]](#3), which prevent pagerank memorless point of vue when looking at paths. Two versions are written, the first one reimplements the algorithm for timestamped edges in reverse ensuring that paths taken into account exist. The problem is that it's not really dynamic since everything needs to be recomputed when going from time $t$ to $t+1$. 

**Complexity:** same as temporal pagerank

#### Static version ```temp_pr_linkstr_static```
In this version we apply standard pagerank algorithm on a link stream, weighting the edges in the graph according to their duration:

We also re-use the transition probability introduced in the temporal pagerank algorithm.

**Complexity**

## Programing Language

The code is written in Python. The choice of a high-level programing language is essentialy for simplicity, readability and the too few algorithmic tricks to implement.

## References

<a id="1">[1]</a> 
Langville, A. N., & Meyer, C. D. (2006). Google's PageRank and beyond: The science of search engine rankings. Princeton university press.

<a id="2">[2]</a> 
Rozenshtein, Polina, and Aristides Gionis. "Temporal pagerank." Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2016, Riva del Garda, Italy, September 19-23, 2016, Proceedings, Part II 16. Springer International Publishing, 2016.

<a id="3">[3]</a> 
Latapy, M., Viard, T., & Magnien, C. (2018). Stream graphs and link streams for the modeling of interactions over time. Social Network Analysis and Mining, 8, 1-29.


