from __future__ import annotations


def is_probable_prime(n: int) -> bool:
    """Deterministic primality test for practical ISS test cases.

    This is intentionally simple for the first slice.
    It is not a general-purpose high-performance primality engine.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    candidate = 5
    step = 2

    while candidate * candidate <= n:
        if n % candidate == 0:
            return False
        candidate += step
        step = 6 - step

    return True


def local_prime_candidates(center: int, radius: int) -> list[int]:
    """Return prime candidates inside [center-radius, center+radius]."""
    lower = max(2, center - radius)
    upper = center + radius

    return [
        candidate
        for candidate in range(lower, upper + 1)
        if is_probable_prime(candidate)
    ]
