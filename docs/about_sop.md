### Sagardotegi Optimization Problem

In the Sagardotegi Optimization Problem (SOP) the objective is to assign MAEB 2025 authors to sagardotegi tables such that their affinity (per table) is maximized.

### How do we measure affinity?

We have 1️⃣ create a normalized list of keywords per author (based on the keywords of the works in which they participate) to 2️⃣ create embeddings using a Transformer language model ([MiniLM](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased)). Next, 3️⃣ we have computed a similarity matrix between authors using the cosine similarity between authors' embeddings. Finally, 4️⃣ we have set the similarity of each author with itself and with its co-authors to zero and normalized the matrix.

### The objective function

**Notation:**

- $s_{ij}$ is the similarity between author $i$ and $j$, where the first author corresponds to index $1$.
- $N$ refers to the number of authors.
- $T$ is the number of tables.
- $K$ the number of authors per table ($K = N/T$).
- $\sigma$ is a permutation of length $N$, where each item corresponds to an author.
- $\sigma_i$ is the $i$-th item (author) of $\sigma$, where $1$ is the first position.

Then, the objective function value of a solution $\sigma$ is,

$$
f(\sigma) = \sum_{t=1}^{T} \sum_{i,j=(t-1)\cdot K+1}^{t\cdot K} s_{\sigma_i \sigma_j}
$$

Note that $\forall i\in[1, N]\ s_{ii} = 0$, and that $s_{kj} = 0$ if $j$ and $k$ have a paper in common.

The objective of the SOP is to find the solution that maximizes the objective function above. Namely,

$$
  \sigma^* = \underset{\sigma \in \mathbb{S}_N}{\text{arg max}}\ f(\sigma)
$$

:orange-badge[⚠️ NOTE] Although this section starts indices from $1$, the Python implementation of the SOP (`SagardotegiProblem` in `sagardotegi_problem.py`) expects permutations whose items are in the range $[0, N-1]$.

### The MAEB 2025 instance

Although the SOP can be applied to any sagardotegi-congress combination, this challenge considers a single instance of MAEB 2025 authors. Specifically, the size of the instance ($N$) is 133, the number of tables ($T$) is 19, and the number of authors per table ($K$) is 7.
