from __future__ import annotations

from dataclasses import dataclass

import pytest

from iss.engine import StructuralSearchEngine
from iss.models import (
    BoundsReport,
    SearchAttempt,
    SearchBudget,
    StrategyClassification,
)


@dataclass(frozen=True)
class DummyPureStrategy:
    id: str = "dummy_pure"
    classification: StrategyClassification = StrategyClassification(
        iss_type="pure_structural",
        factorization_general=False,
        requires_explicit_opt_in=False,
    )

    def search(self, n: int, budget: SearchBudget) -> SearchAttempt:
        return SearchAttempt(
            strategy_id=self.id,
            status="no_match",
            reason="dummy_no_match",
            classification=self.classification,
            bounds=BoundsReport(
                bounded=True,
                factorization_general=False,
                radius=budget.radius,
                max_candidates=budget.max_candidates,
            ),
        )


@dataclass(frozen=True)
class DummyFactoringAdjacentStrategy:
    id: str = "dummy_factoring_adjacent"
    classification: StrategyClassification = StrategyClassification(
        iss_type="factoring_adjacent",
        factorization_general=False,
        requires_explicit_opt_in=True,
    )

    def search(self, n: int, budget: SearchBudget) -> SearchAttempt:
        return SearchAttempt(
            strategy_id=self.id,
            status="matched",
            reason="dummy_match",
            classification=self.classification,
            bounds=BoundsReport(
                bounded=True,
                factorization_general=False,
                radius=budget.radius,
                max_candidates=budget.max_candidates,
            ),
            payloads=[{"kind": "dummy_payload", "input_n": str(n)}],
        )


def test_engine_rejects_factoring_adjacent_by_default() -> None:
    engine = StructuralSearchEngine([DummyFactoringAdjacentStrategy()])

    result = engine.search(3465924001)

    assert result.status == "no_match"
    assert len(result.attempts) == 1

    attempt = result.attempts[0]
    assert attempt.status == "rejected"
    assert attempt.reason == "strategy_requires_explicit_opt_in"
    assert attempt.classification.iss_type == "factoring_adjacent"


def test_engine_allows_factoring_adjacent_with_explicit_opt_in() -> None:
    engine = StructuralSearchEngine([DummyFactoringAdjacentStrategy()])

    result = engine.search(
        3465924001,
        budget=SearchBudget(allow_factoring_adjacent=True),
    )

    assert result.status == "matched"
    assert result.attempts[0].status == "matched"


def test_engine_runs_pure_structural_by_default() -> None:
    engine = StructuralSearchEngine([DummyPureStrategy()])

    result = engine.search(3465924001)

    assert result.status == "no_match"
    assert result.attempts[0].status == "no_match"
    assert result.attempts[0].classification.iss_type == "pure_structural"


def test_engine_rejects_invalid_input() -> None:
    engine = StructuralSearchEngine([DummyPureStrategy()])

    with pytest.raises(ValueError, match="greater than 1"):
        engine.search(1)


def test_result_serializes_big_ints_as_strings() -> None:
    engine = StructuralSearchEngine([DummyPureStrategy()])

    result = engine.search(100000002790000029250000142519000317757090255987171)
    data = result.to_json_dict()

    assert data["input_n"] == "100000002790000029250000142519000317757090255987171"
    assert data["summary"]["matched"] is False
    assert data["summary"]["strategies_attempted"] == 1
