from __future__ import annotations

from iss.engine import StructuralSearchEngine
from iss.models import SearchBudget
from iss.strategies.log_scale_semiprime import LogScaleSemiprimeStrategy


def build_engine() -> StructuralSearchEngine:
    return StructuralSearchEngine([LogScaleSemiprimeStrategy(max_denominator=8)])


def test_probe_fixture_unbalanced_semiprime_matches_with_declared_radius() -> None:
    n = 3465924001
    engine = build_engine()

    result = engine.search(n, budget=SearchBudget(radius=16))

    assert result.status == "matched"
    assert result.attempts[0].status == "matched"

    payload = result.attempts[0].payloads[0].to_json_dict()

    assert payload["strategy"]["id"] == "log_scale_semiprime"
    assert payload["strategy"]["profile"] == [1, 1]
    assert payload["strategy"]["scales"] == ["1/5", "4/5"]
    assert payload["support"][0]["base"] == "71"
    assert payload["support"][1]["base"] == "48815831"
    assert payload["verification"]["product_equals_input"] is True
    assert payload["bounds"]["bounded"] is True
    assert payload["bounds"]["factorization_general"] is False


def test_probe_fixture_unbalanced_semiprime_fails_with_too_small_radius() -> None:
    n = 3465924001
    engine = build_engine()

    result = engine.search(n, budget=SearchBudget(radius=4))

    assert result.status == "no_match"
    assert result.attempts[0].status == "no_match"
    assert result.attempts[0].reason == "no_dividing_local_prime_found"
    assert result.attempts[0].bounds.bounded is True
    assert result.attempts[0].bounds.factorization_general is False


def test_probe_fixture_randomish_21_byte_number_fails_cleanly() -> None:
    n = 123456789987654321123456789987654321123456789
    engine = build_engine()

    result = engine.search(n, budget=SearchBudget(radius=16))

    assert result.status == "no_match"
    assert result.attempts[0].status in {"no_match", "budget_exhausted"}
    assert result.attempts[0].bounds.bounded is True
    assert result.attempts[0].bounds.factorization_general is False
    assert result.attempts[0].payloads == []


def test_probe_fixture_squarefree_k5_is_not_claimed_by_semiprime_strategy() -> None:
    n = 100000002790000029250000142519000317757090255987171
    engine = build_engine()

    result = engine.search(n, budget=SearchBudget(radius=16))

    assert result.status == "no_match"
    assert result.attempts[0].status in {"no_match", "budget_exhausted"}
    assert result.attempts[0].bounds.bounded is True
    assert result.attempts[0].bounds.factorization_general is False
    assert result.attempts[0].payloads == []
