from sagardotegi_problem import SagardotegiProblem
import numpy as np


def evaluate_solution(solution):
    solution = np.array(solution).astype(int)

    problem = SagardotegiProblem(table_size=7)

    assert problem.check_solution(solution), f"The solution must be a permutation of size {problem.size}"

    return problem.evaluate(solution)
