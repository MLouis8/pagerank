# Temporal PageRank

The objective of this little project is to explore the pagerank algorithm and its temporal versions.

## Content

The algorithms are implemented [here](./src/pagerank.py)

#### Original Pagerank
The basic pagerank [[1]](#1) is implemented as a reference algorithm to test convergence of the other algorithms when all time features are equal. It also gives a benchmark for the performances. The basic Aitken extrapolation improvement is implemented and detailed here, as an exemple of possible accelerations.

**Complexity:** $O(n^2)$ but with sparse hyperlink matrices it is nearly linear.

#### Temporal Pagerank
It's the algorithm from [[2]](#2). It works on temporal edges where only the starting time is given, we call this edges *timestamped edges*.
Here, the random walk point of vue is taken and the temporal pagerank for a node $u$ at time $t$ is:
$$r(u, t) = \sum_{v \in V} \sum_{k=0}^{t}$$

**Complexity:**

#### Temporal Pagerank on link streams
On this algorithm, the edges have now also an ending time [[3]](#3), which prevent pagerank memorless point of vue when looking at paths. Two versions are written, the first one reimplements the algorithm for timestamped edges in reverse ensuring that paths taken into account exist. The problem is that it's not really dynamic since everything needs to be recomputed when going from time $t$ to $t+1$. The second version face the path vanishing problem by weighting them according to their time duration.

**Complexity:** same as temporal pagerank

## Tests

The test are [here](./test/test.py).

## Programing Language

The code is written in Python. The choice of a high-level programing language is essentialy for simplicity, readability and the too few algorithmic tricks to implement.

## References

<a id="1">[1]</a> 
Langville, A. N., & Meyer, C. D. (2006). Google's PageRank and beyond: The science of search engine rankings. Princeton university press.

<a id="2">[2]</a> 
Rozenshtein, Polina, and Aristides Gionis. "Temporal pagerank." Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2016, Riva del Garda, Italy, September 19-23, 2016, Proceedings, Part II 16. Springer International Publishing, 2016.

<a id="3">[3]</a> 
Latapy, M., Viard, T., & Magnien, C. (2018). Stream graphs and link streams for the modeling of interactions over time. Social Network Analysis and Mining, 8, 1-29.


