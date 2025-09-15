from typing import Iterable, List, Optional, Tuple, Union

Number = int  # per spec: integers only

class InputError(ValueError):
    pass

def _validate_array(A: Iterable[Union[int, bool]]) -> List[int]:
    if A is None:
        raise InputError("Array is None.")
    try:
        B = list(A)
    except TypeError as e:
        raise InputError("Array is not iterable.") from e
    if len(B) < 3:
        raise InputError("Array must have length ≥ 3.")
    # enforce integers
    for x in B:
        if not isinstance(x, int) or isinstance(x, bool):
            raise InputError("All elements must be integers.")
    return B

def three_sum_bruteforce(
    A: Iterable[int],
    target: int,
    return_triplet: bool = True
) -> Tuple[bool, Optional[Tuple[int, int, int]], int]:
    """
    Brute-force ThreeSum. Three nested loops. Distinct indices via bounds.
    Operation counted = one triplet sum check.
    Returns: (found, triplet_or_None, ops)
    """
    B = _validate_array(A)
    if not isinstance(target, int) or isinstance(target, bool):
        raise InputError("Target must be an integer.")

    n = len(B)
    ops = 0
    for i in range(0, n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                ops += 1
                s = B[i] + B[j] + B[k]
                if s == target:
                    if return_triplet:
                        return True, (B[i], B[j], B[k]), ops
                    return True, None, ops
    return False, None, ops
