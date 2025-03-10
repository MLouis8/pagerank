# Temporal PageRank

The objective of this project is to explore the pagerank algorithm and its temporal versions. First the **original algorithm** is implemented, then 3 others follow. The second one is the **temporal pagerank** [[2]](#2) applied on edges with only one time parameter. It takes temporal edges one by one, allowing the user to have the temporal pagerank vector a each time step, in this sense it really gives us a temporal pagerank. Then the focus was put on **linkstreams** [[3]](#3) where edges also have an expiry time. It makes it impossible to simply update existing walks when adding an edge as before, since as time goes by, edges can be removed and paths destroyed. Hence we implemented two solutions, the first is a direct adaptation of temporal pagerank, where only existing edges at a specific time are considered. But in this way we lose the dynamic essence of the algorithm (if an edge needs to be added, everything must be computed again). The second solution is a pagerank like measure merging the original algorithm with concepts of link streams.

## Content

### Original Pagerank [```static_pr_pwr```](./src/pagerank.py)

The basic pagerank [[1]](#1) with the power method is implemented as a reference algorithm and is needed for the pagerank like measure for linkstreams.
It computes the pagerank vector $\pi^k$ at $k$-th iteration such that:

$$\pi^{k+1} = \alpha \pi^k \cdot H + (\alpha \pi^k \cdot a + 1-\alpha) p$$

with $\pi^0$ an arbitrary vector, $\alpha$ the jumping probability, $a$ the dangling node vector, $H$ the stochastic matrix of transitions in the graph and $p$ the personalization vector.

**Complexity:** $O(n^2)$ but with sparse hyperlink matrices it is nearly linear.

### Temporal Pagerank [```temp_pr_tstamp_rdwalk```](./src/pagerank.py)

It's the algorithm from [[2]](#2). It works on temporal edges where only the starting time is given, we call this edges *timestamped edges*.
Here, the random walk point of vue is taken so the objective is to count all possible walks and update them as new edges arrive. The temporal pagerank for a node $u$ at time $t$ is:

$$r(u, t) = \sum_{v \in V} \sum_{k=0}^{t} (1-\alpha)\alpha^k \sum_{z\in Z(v, u | t) \wedge |z| = k} Pr[z\ |\ t]$$

Knowing that:

- $Z(v, u|t)$ is the set of all temporal walks (walks where edges are ordered by timestamp) that start at node $v$ and reach $u$ before $t$
- $Pr[z|t]$ is the proportion of temporal walks of size $|z|$ starting from $u$ to $v$ compared to all temporal walks of size $|z|$.

**Complexity:** The implementation is linear in the number of edges with one or two pass (whether a personalization vector is used or not).

### Temporal Pagerank on link streams [```temp_pr_linkstr_walk```](./src/pagerank.py)

The idea is use the algorithm above on the edges existing at a specific time $t$.

**Complexity** Same as temporal Pagerank.

### Pagerank like measure on link streams [```temp_pr_linkstr```](./src/pagerank.py)

It is the original pagerank that is used, on a graph where edges are weighted according to their *duration* (timespan / entire time interval).

## Experimentations

### Convergence

We first want to verify the convergence properties of the temporal pagerank towards static orginal pagerank under specific conditions.
For this we use the personalization vector where nodes are weighted according to the number of out edges they have in proportion to the total numer of edges.
Convergence appear when edges are drawn randomly and the bigger the size of the sample, the closer it comes to static pagerank.

![convergence](plots/convergence.jpg)

Here we used the temporal graph ```hyper_text```[[4]](#4) that has $113$ nodes and $41636$ temporal edges and Pearson correlation coefficient to compare at each edge addition static pagerank and temporal pagerank.
The convergence is observable as the correlation tend to $1$.

### Pagerank analysis

Let's now run the above algorithms on the same dataset. For link streams, end timestamps are drawn as random and starting timestamps are kept. We follow here the ranks of the node with the biggest static pagerank over time.

![comparison](plots/pr_comparisons.jpg)

Temporal pagerank shows significant evolutions in ranking while other two metrics vary much less. In a sense this result could be expected for the pagerank like measure in link streams (green) since just weights on edges are added (the structure of the graph is the same). But the linkstream adaptation has no particular reason to follow static ranking, with furthermore analysis we could find interesting explanations to this.

## Programing Language

The code is written in Python. The choice of a high-level programing language is essentialy for simplicity, readability and the too few algorithmic tricks to implement.

## References

<a id="1">[1]</a>
Langville, A. N., & Meyer, C. D. (2006). Google's PageRank and beyond: The science of search engine rankings. Princeton university press.

<a id="2">[2]</a>
Rozenshtein, Polina, and Aristides Gionis. "Temporal pagerank." Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2016, Riva del Garda, Italy, September 19-23, 2016, Proceedings, Part II 16. Springer International Publishing, 2016.

<a id="3">[3]</a>
Latapy, M., Viard, T., & Magnien, C. (2018). Stream graphs and link streams for the modeling of interactions over time. Social Network Analysis and Mining, 8, 1-29.

<a id="3">[4]</a>
https://github.com/piluc/TWBC/blob/main/graphs/1_01_hypertext.patg