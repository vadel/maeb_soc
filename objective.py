def evaluate_solution(solution):
    # Dummy scoring: lower difference between index and value = higher score
    score = sum(abs(i - val) for i, val in enumerate(solution))
    return 100 - score  # Higher is better

