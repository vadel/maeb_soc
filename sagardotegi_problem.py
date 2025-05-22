import numpy as np
from numpy.typing import NDArray


class SagardotegiProblem:
    """Main class of the Sagardotegi Optimization Problem."""

    def __init__(
        self,
        similarity_matrix_filename: str = "instance.txt",
        author_names_filename: str = "author_names.txt",
        table_size: int = 7,
    ):
        # deserialize similarity matrix
        self.mat = np.loadtxt(similarity_matrix_filename, delimiter=",")
        self.size = self.mat.shape[0]
        self.table_size = table_size

        assert self.size % self.table_size == 0, (
            f"The number of authors ({self.size}) must be divisible by the number of tables ({self.table_size})"
        )

        # load the (ordered list of samples)
        with open(author_names_filename, "r", encoding="utf-8") as f:
            self.author_names = [line.strip() for line in f if line.strip()]

    def check_solution(self, p: NDArray):
        """Returns `True` if the input numpy array is a valid solution and `False` otherwise."""
        return  p.size == self.size and np.unique(p).size == self.size and (np.unique(p) == np.arange(p.size)).all()

    def evaluate(self, p: NDArray):
        """Computes the objective function value (fitness) of the input solution."""

        def table_sim(idxs):
            submat = self.mat[idxs][:, idxs]
            return submat.sum()

        splitted = p.reshape((-1, self.table_size))
        tables_sim = np.apply_along_axis(table_sim, 1, splitted)
        return np.sum(tables_sim)

    def solution_to_layout(self, solution: NDArray, print_stdout: bool = True):
        """Prints the table layout specified by the input solution."""
        s = ""
        names = np.array(self.author_names)
        j = 1
        for i, name in enumerate(names[solution]):
            if i % self.table_size == 0:
                s += f"\n### Table {j}\n"
                j += 1
            s += f"- {name}\n"
        if print_stdout:
            print(s)
        return s

    def visualize_solution(self, solution: NDArray, plot: bool = True):
        """Visualizes the solution using networkx and matplotlib."""
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        G.add_nodes_from(self.author_names)

        edges_with_weights = []
        for i in range(self.size):
            for j in range(i + 1, self.size):
                weight = self.mat[i, j]
                edges_with_weights.append((self.author_names[i], self.author_names[j], {"weight": weight}))

        G.add_edges_from(edges_with_weights)

        # Compute the layout based on edge weights (similarity)
        # k is the optimal distance between nodes.
        pos = nx.spring_layout(G, k=1/np.sqrt(self.size), iterations=1000, weight="weight")

        fig = plt.figure(figsize=(12, 10))

        # only draw the nodes
        tables = np.arange(self.size // self.table_size).repeat(self.table_size)
        ordered_tables = np.empty((self.size))
        for i in range(self.size):
            ordered_tables[solution[i]] = tables[i]

        nx.draw_networkx_nodes(G, pos, node_size=100, cmap=plt.get_cmap("tab20"), alpha=0.9, node_color=ordered_tables) # Adjust node_size and cmap as desired

        # daw labels (author names)
        nx.draw_networkx_labels(G, pos, font_size=8)

        fs = self.evaluate(solution)

        plt.title(f"Sagardotegi Layout (fitness: {round(fs, 2)})")
        plt.axis("off")
        plt.tight_layout()

        if plot:
            plt.show()

        return fig


if __name__ == "__main__":
    import time

    problem = SagardotegiProblem(table_size=7)
    # problem = SagardotegiProblem(table_size=19)

    best_solution = np.random.permutation(problem.size)
    best_fs = problem.evaluate(best_solution)

    start = time.time()
    i = 0
    try:
        while True:
            i += 1
            solution = np.random.permutation(problem.size)
            fs = problem.evaluate(solution)
            if fs > best_fs:
                t = time.time() - start
                print(f"🙌 Best solution improved! fitness={round(fs, 3)}, iteration={i}, elapsed={round(t, 2)}s")
                best_fs = fs
                best_solution = solution

    except KeyboardInterrupt:
        print("\n-------------------------")
        print("\n👹 Random search stopped. Best solution is:")
        print()
        print(best_solution)
        problem.solution_to_layout(best_solution)
        problem.visualize_solution(best_solution)
