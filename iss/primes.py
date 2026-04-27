from __future__ import annotations


_SMALL_PRIMES = (
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
)


def is_probable_prime(n: int) -> bool:
    """Return whether n is probably prime using Miller-Rabin.

    This is a verification-layer primitive.

    It must not be used as a factor search strategy. ISS strategies may use it
    only to validate bounded candidates produced by declared structural probes.
    """
    if n < 2:
        return False

    for prime in _SMALL_PRIMES:
        if n == prime:
            return True
        if n % prime == 0:
            return False

    d = n - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    for base in bases:
        if base >= n:
            continue

        if _is_composite_witness(base, d, s, n):
            return False

    return True


def _is_composite_witness(base: int, d: int, s: int, n: int) -> bool:
    x = pow(base, d, n)

    if x == 1 or x == n - 1:
        return False

    for _ in range(s - 1):
        x = pow(x, 2, n)

        if x == n - 1:
            return False

    return True


def local_prime_candidates(center: int, radius: int) -> list[int]:
    """Return probable-prime candidates inside [center-radius, center+radius].

    The candidate window is structural and bounded. This helper must not be
    generalized into scanning divisors from 2 upward.
    """
    lower = max(2, center - radius)
    upper = center + radius

    return [
        candidate
        for candidate in range(lower, upper + 1)
        if is_probable_prime(candidate)
    ]
