import random
from typing import List, Tuple

def random_distinct_array(n: int, lo: int = -10**6, hi: int = 10**6) -> List[int]:
    # sample distinct ints; ensure range is wide enough
    if hi - lo + 1 < n:
        hi = lo + n + 10
    return random.sample(range(lo, hi), n)

def make_mix_cases(
    sizes=(50, 100, 200, 400, 800),
    seed: int = 1337
) -> Tuple[list, list]:
    """
    For each n, create two arrays:
      - solvable: plant a guaranteed triplet
      - unsolvable: random; probability of solution low but not zero
    Returns (cases, labels) with parallel lists.
    """
    random.seed(seed)
    cases, labels = [], []
    for n in sizes:
        arr = random_distinct_array(n)
        # plant solution in a copy
        arr_sol = arr[:]
        a, b, c = arr_sol[0], arr_sol[1], arr_sol[2]
        t = a + b + c
        cases.append((arr_sol, t))
        labels.append(f"n={n}_solvable")

        # unsolvable target attempt: pick a value outside 3*range
        t_bad = 3 * (10**7)
        cases.append((arr, t_bad))
        labels.append(f"n={n}_unsolvable")
    return cases, labels
