# Temporal PageRank

The objective of this little project is to explore the pagerank algorithm and its temporal versions.

## Content

The following algorithms are implemented [here](./src/pagerank.py)

#### Original Pagerank
The basic pagerank is implemented as a reference algorithm to test convergence of the other algorithms when all time features are equal. It also gives a benchmark for the performances.

#### Temporal Pagerank
It's the algorithm from [[1]](#1). It works on temporal edges where only the starting time is given, we call this edges "timestamped edges".

#### Temporal Pagerank on link streams
On this algorithm, the edges have now also an ending time, which prevent pagerank memorless point of vue when looking at paths. Two versions are written, the first one reimplements the algorithm for timestamped edges in reverse ensuring that paths taken into account exist. The problem is that it's not really dynamic since everything needs to be recomputed when going from time $t$ to $t+1$. The second version face the path vanishing problem by weighting them according to their time duration.

## Tests

The test are [here](./test/test.py).

## Programing Language

The code is written in Python. The choice of a high-level programing language is essentialy for simplicity, readability and the absence of interesting algorithmic tricks to improve complexity in the programs.

## References

<a id="1">[1]</a> 
Rozenshtein, Polina, and Aristides Gionis. "Temporal pagerank." Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2016, Riva del Garda, Italy, September 19-23, 2016, Proceedings, Part II 16. Springer International Publishing, 2016.


