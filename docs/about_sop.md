In the Sagardotegi Optimization Problem (SOP) the objective is to assign MAEB 2025 authors to sagardotegi tables such that their affinity (per table) is maximized.

**How do we measure affinity?**

We have 1️⃣ create a normalized list of keywords per author (based on the keywords of the works in which they participate) to 2️⃣ create embeddings using a Transformer language model ([MiniLM](https://huggingface.co/microsoft/MiniLM-L12-H384-uncased)). Next, 3️⃣ we have computed a similarity matrix between authors using the cosine similarity between authors' embeddings. Finally, 4️⃣ we have set the similarity of each author with itself and with its co-authors to zero and normalized the matrix.

**The objective function:**

Notation:

- $s_{ij}$ is the similarity between author $i$ and $j$, where the first author corresponds to index $0$.
- $N$ refers to the number of authors.
- $T$ is the number of tables.
- $K$ the number of authors per table ($K = N/T$).
- $\sigma$ is a permutation of length $N$.
- $\sigma_i$ is the $i$-th item of $\sigma$, where $0$ is the first position.

Then, the objective function value of a solution $\sigma$ is,

$$
f(\sigma) = \sum_{t=0}^{T-1} \sum_{i,j=t\cdot K}^{(t+1)\cdot K-1} s_{\sigma_i \sigma_j}
$$

And the objective of the SOP is to find the solution that maximizes the objective function above. Namely,

$$
  \sigma^* = \underset{\sigma \in \mathbb{S}_N}{\text{arg max}} f(\sigma)
$$
