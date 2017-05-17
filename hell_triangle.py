"""Hell Triangle Challenge."""

from typing import Sequence, Tuple
from functools import lru_cache

Row = Sequence[int]
Triangle = Sequence[Row]


def split(tri: Triangle) -> Tuple[Triangle, Triangle]:
    """Return the left and right subtriangles as (left, right)."""
    left_right_pairs = ((row[:-1], row[1:]) for row in tri[1:])
    left, right = zip(*left_right_pairs)  # Unzip pairs
    return (left, right)


def max_path(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    if len(tri) == 1:
        return tri[0][0]

    left, right = split(tri)
    return tri[0][0] + max(max_path(left), max_path(right))


def max_path_cached(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    last_row_index = len(tri) - 1

    @lru_cache(maxsize=None)  # Avoid repetitive calculations
    def max_path_from(i: int, j: int) -> int:
        """Return the maximum possible sum from subtriangle [i][j]."""
        if i < last_row_index:
            left = max_path_from(i + 1, j)
            right = max_path_from(i + 1, j + 1)
            return tri[i][j] + max(left, right)
        return tri[i][j]

    return max_path_from(0, 0)


def max_path_iterative(tri: Triangle) -> int:
    """Return the maximum sum on a path from top to bottom."""
    below_max = (0,) * len(tri[-1])  # Initialize to a row of zeros
    for row in reversed(tri):
        acc_row = tuple(bm + r for bm, r in zip(below_max, row))
        below_max = tuple(max(acc_row[i - 1], acc_row[i])
                          for i in range(1, len(acc_row)))
    return acc_row[0]
