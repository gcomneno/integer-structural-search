from __future__ import annotations


def integer_nth_root_floor(n: int, degree: int) -> int:
    """Return floor(n ** (1 / degree)) using integer arithmetic."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if degree <= 0:
        raise ValueError("degree must be positive")

    if n in (0, 1):
        return n

    low = 1
    high = 1

    while high**degree <= n:
        high *= 2

    while low + 1 < high:
        mid = (low + high) // 2
        value = mid**degree

        if value <= n:
            low = mid
        else:
            high = mid

    return low
