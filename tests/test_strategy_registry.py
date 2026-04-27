from __future__ import annotations

from dataclasses import dataclass

import pytest

from iss.models import BoundsReport, SearchAttempt, SearchBudget, StrategyClassification
from iss.registry import StrategyRegistry


@dataclass(frozen=True)
class DummyStrategy:
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


def test_registry_registers_and_gets_strategy() -> None:
    registry = StrategyRegistry()
    strategy = DummyStrategy(id="dummy")

    registry.register(strategy)

    assert registry.get("dummy") is strategy


def test_registry_rejects_duplicate_strategy_ids() -> None:
    registry = StrategyRegistry()

    registry.register(DummyStrategy(id="dummy"))

    with pytest.raises(ValueError, match="Strategy already registered: dummy"):
        registry.register(DummyStrategy(id="dummy"))


def test_registry_reports_unknown_strategy_id() -> None:
    registry = StrategyRegistry()

    with pytest.raises(KeyError, match="Unknown strategy: missing"):
        registry.get("missing")


def test_registry_lists_strategy_ids_sorted() -> None:
    registry = StrategyRegistry()

    registry.register(DummyStrategy(id="zeta"))
    registry.register(DummyStrategy(id="alpha"))

    assert registry.ids() == ["alpha", "zeta"]


def test_registry_returns_all_strategies() -> None:
    registry = StrategyRegistry()
    alpha = DummyStrategy(id="alpha")
    zeta = DummyStrategy(id="zeta")

    registry.register(alpha)
    registry.register(zeta)

    assert registry.all() == [alpha, zeta]


def test_engine_can_be_created_from_registry() -> None:
    from iss.engine import StructuralSearchEngine

    registry = StrategyRegistry()
    strategy = DummyStrategy(id="dummy")
    registry.register(strategy)

    engine = StructuralSearchEngine.from_registry(registry)

    result = engine.search(3465924001)

    assert result.status == "no_match"
    assert result.attempts[0].strategy_id == "dummy"
