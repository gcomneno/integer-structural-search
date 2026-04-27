from __future__ import annotations

from iss.primes import is_probable_prime, local_prime_candidates


def test_is_probable_prime_accepts_known_prime() -> None:
    assert is_probable_prime(48815831) is True


def test_is_probable_prime_rejects_known_composite() -> None:
    assert is_probable_prime(48815831 * 71) is False


def test_local_prime_candidates_uses_bounded_window() -> None:
    candidates = local_prime_candidates(center=80, radius=16)

    assert 71 in candidates
    assert all(64 <= candidate <= 96 for candidate in candidates)


def test_local_prime_candidates_handles_large_center_without_factor_search() -> None:
    candidates = local_prime_candidates(
        center=100000000000000000000000,
        radius=4,
    )

    assert isinstance(candidates, list)
