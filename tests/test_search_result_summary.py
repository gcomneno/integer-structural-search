from __future__ import annotations

from dataclasses import dataclass

from iss.engine import StructuralSearchEngine
from iss.models import BoundsReport, SearchAttempt, SearchBudget, StrategyClassification


@dataclass(frozen=True)
class DummyMatchedStrategy:
    id: str
    classification: StrategyClassification = StrategyClassification(
        iss_type="pure_structural",
        factorization_general=False,
        requires_explicit_opt_in=False,
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
            ),
            payloads=[],
        )


@dataclass(frozen=True)
class DummyNoMatchStrategy:
    id: str
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
            ),
        )


def test_search_result_summary_reports_matched_strategy_ids() -> None:
    engine = StructuralSearchEngine(
        [
            DummyNoMatchStrategy(id="first_no_match"),
            DummyMatchedStrategy(id="first_match"),
            DummyMatchedStrategy(id="second_match"),
        ]
    )

    result = engine.search(3465924001)
    data = result.to_json_dict()

    assert data["summary"]["matched"] is True
    assert data["summary"]["strategies_attempted"] == 3
    assert data["summary"]["matches_count"] == 2
    assert data["summary"]["matched_strategy_ids"] == [
        "first_match",
        "second_match",
    ]
    assert data["summary"]["factorization_general"] is False


def test_search_result_summary_reports_empty_matches_on_no_match() -> None:
    engine = StructuralSearchEngine(
        [
            DummyNoMatchStrategy(id="first_no_match"),
            DummyNoMatchStrategy(id="second_no_match"),
        ]
    )

    result = engine.search(3465924001)
    data = result.to_json_dict()

    assert data["summary"]["matched"] is False
    assert data["summary"]["strategies_attempted"] == 2
    assert data["summary"]["matches_count"] == 0
    assert data["summary"]["matched_strategy_ids"] == []
    assert data["summary"]["factorization_general"] is False
