### Sagardotegi Optimization Problem

In the Sagardotegi Optimization Problem (SOP) the objective is to assign MAEB 2025 authors to sagardotegi tables such that their affinity (per table) is maximized.

### The objective function

**Notation:**

- $N$ refers to the number of authors.
- $T$ is the number of tables.
- $K$ the number of authors per table ($K = N/T$).
- $\sigma$ is a permutation of length $N$, where each item corresponds to an author.
- $\sigma_i$ is the $i$-th item (author) of $\sigma$.
- $s_{ij}$ is the similarity between author $i$ and $j$.
- $0\leq i,j \leq N-1$.

Each table is assigned a consecutive block of $K$ authors in the permutation $\sigma$. That is, authors $(\sigma_0$, ..., $\sigma_{K-1})$ sit at table 1, authors $(\sigma_K$, ..., $\sigma_{2K-1})$ at table 2, and so on, until all $T$ tables are filled.

Thus, the objective function value of a solution $\sigma$ is,

$$
f(\sigma) = \sum_{t=1}^{T} \sum_{i,j=(t-1)\cdot K}^{t\cdot K -1 } s_{\sigma_i \sigma_j}
$$

The objective of the SOP is to find the solution that maximizes the objective function above. Namely,

$$
  \sigma^* = \underset{\sigma \in \mathbb{S}_N}{\text{arg max}}\ f(\sigma)
$$


### Restrictions

:orange-badge[⚠️ NOTE] $\ \forall i \in[0, N-1], \  s_{ii} = 0$. 

:orange-badge[⚠️ NOTE] $\ \forall i,j \in[0, N-1], \ s_{ij} = 0$ if $j$ and $k$ have a paper in common.

:orange-badge[⚠️ NOTE] $\ $ We expect permutations whose items are in the range $[0, N-1]$.

### The MAEB 2025 instance

Although the SOP can be applied to any sagardotegi-congress combination, this challenge considers a single instance of MAEB 2025 authors. Specifically:
- The size of the instance ($N$) is 133.
- The number of tables ($T$) is 19.
- The number of authors per table ($K$) is 7.

