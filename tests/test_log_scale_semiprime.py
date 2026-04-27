from __future__ import annotations

from iss.engine import StructuralSearchEngine
from iss.models import SearchBudget
from iss.strategies.log_scale_semiprime import LogScaleSemiprimeStrategy


def test_log_scale_semiprime_finds_unbalanced_case() -> None:
    n = 3465924001
    engine = StructuralSearchEngine([LogScaleSemiprimeStrategy(max_denominator=8)])

    result = engine.search(n, budget=SearchBudget(radius=16))

    assert result.status == "matched"
    assert len(result.attempts) == 1

    attempt = result.attempts[0]
    assert attempt.status == "matched"
    assert attempt.classification.iss_type == "pure_structural"
    assert attempt.bounds.factorization_general is False

    payload = attempt.payloads[0].to_json_dict()
    assert payload["strategy"]["id"] == "log_scale_semiprime"
    assert payload["strategy"]["profile"] == [1, 1]
    assert payload["strategy"]["scales"] == ["1/5", "4/5"]
    assert payload["support"][0]["base"] == "71"
    assert payload["support"][1]["base"] == "48815831"
    assert payload["verification"]["product_equals_input"] is True
    assert payload["verification"]["prime_checks"] is True
    assert payload["bounds"]["bounded"] is True
    assert payload["bounds"]["factorization_general"] is False


def test_log_scale_semiprime_radius_too_small_fails_cleanly() -> None:
    n = 3465924001
    engine = StructuralSearchEngine([LogScaleSemiprimeStrategy(max_denominator=8)])

    result = engine.search(n, budget=SearchBudget(radius=4))

    assert result.status == "no_match"
    assert result.attempts[0].status == "no_match"
    assert result.attempts[0].reason == "no_dividing_local_prime_found"
    assert result.attempts[0].bounds.bounded is True
    assert result.attempts[0].bounds.factorization_general is False


def test_log_scale_semiprime_respects_candidate_budget() -> None:
    n = 3465924001
    engine = StructuralSearchEngine([LogScaleSemiprimeStrategy(max_denominator=8)])

    result = engine.search(n, budget=SearchBudget(radius=16, max_candidates=1))

    assert result.status == "no_match"
    assert result.attempts[0].status == "budget_exhausted"
    assert result.attempts[0].reason == "max_candidates_exceeded"


def test_log_scale_semiprime_returns_structural_payload_dataclass() -> None:
    n = 3465924001
    engine = StructuralSearchEngine([LogScaleSemiprimeStrategy(max_denominator=8)])

    result = engine.search(n, budget=SearchBudget(radius=16))

    payload = result.attempts[0].payloads[0]

    assert payload.kind == "structural_payload"
    assert payload.input_n == "3465924001"
    assert payload.strategy.id == "log_scale_semiprime"
    assert payload.support[0].base == "71"
    assert payload.support[1].base == "48815831"
