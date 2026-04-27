from __future__ import annotations

from iss.engine import StructuralSearchEngine
from iss.models import SearchBudget
from iss.strategies.balanced_root_scale import BalancedRootScaleSemiprimeStrategy


def test_balanced_root_scale_finds_balanced_semiprime() -> None:
    n = 10007 * 10009
    engine = StructuralSearchEngine([BalancedRootScaleSemiprimeStrategy()])

    result = engine.search(n, budget=SearchBudget(radius=2))

    assert result.status == "matched"
    assert result.attempts[0].status == "matched"

    payload = result.attempts[0].payloads[0].to_json_dict()

    assert payload["strategy"]["id"] == "balanced_root_scale_semiprime"
    assert payload["strategy"]["family"] == "balanced-root-scale"
    assert payload["strategy"]["profile"] == [1, 1]
    assert payload["strategy"]["scales"] == ["1/2", "1/2"]
    assert payload["support"][0]["base"] == "10007"
    assert payload["support"][1]["base"] == "10009"
    assert payload["verification"]["product_equals_input"] is True
    assert payload["verification"]["prime_checks"] is True
    assert payload["bounds"]["bounded"] is True
    assert payload["bounds"]["factorization_general"] is False


def test_balanced_root_scale_does_not_find_unbalanced_semiprime() -> None:
    n = 3465924001
    engine = StructuralSearchEngine([BalancedRootScaleSemiprimeStrategy()])

    result = engine.search(n, budget=SearchBudget(radius=16))

    assert result.status == "no_match"
    assert result.attempts[0].status == "no_match"
    assert result.attempts[0].reason == "no_dividing_local_prime_found"
    assert result.attempts[0].bounds.bounded is True
    assert result.attempts[0].bounds.factorization_general is False
    assert result.attempts[0].payloads == []


def test_balanced_root_scale_respects_candidate_budget() -> None:
    n = 10007 * 10009
    engine = StructuralSearchEngine([BalancedRootScaleSemiprimeStrategy()])

    result = engine.search(n, budget=SearchBudget(radius=16, max_candidates=0))

    assert result.status == "no_match"
    assert result.attempts[0].status == "budget_exhausted"
    assert result.attempts[0].reason == "max_candidates_exceeded"


def test_balanced_root_scale_payload_is_structural_dataclass() -> None:
    n = 10007 * 10009
    engine = StructuralSearchEngine([BalancedRootScaleSemiprimeStrategy()])

    result = engine.search(n, budget=SearchBudget(radius=2))
    payload = result.attempts[0].payloads[0]

    assert payload.kind == "structural_payload"
    assert payload.strategy.id == "balanced_root_scale_semiprime"
    assert payload.support[0].base == "10007"
    assert payload.support[1].base == "10009"
