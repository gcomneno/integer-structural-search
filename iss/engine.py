from __future__ import annotations

from typing import Protocol

from iss.models import (
    BoundsReport,
    SearchAttempt,
    SearchBudget,
    SearchResult,
    StrategyClassification,
)


class StructuralStrategy(Protocol):
    id: str
    classification: StrategyClassification

    def search(self, n: int, budget: SearchBudget) -> SearchAttempt:
        ...


class StructuralSearchEngine:
    def __init__(self, strategies: list[StructuralStrategy]) -> None:
        self._strategies = {strategy.id: strategy for strategy in strategies}

    @classmethod
    def from_registry(cls, registry) -> StructuralSearchEngine:
        return cls(registry.all())

    def search(
        self,
        n: int,
        budget: SearchBudget | None = None,
        strategy_ids: list[str] | None = None,
    ) -> SearchResult:
        if n <= 1:
            raise ValueError("ISS input must be an integer greater than 1")

        budget = budget or SearchBudget()
        selected_ids = strategy_ids or list(self._strategies)

        attempts: list[SearchAttempt] = []

        for strategy_id in selected_ids:
            strategy = self._strategies[strategy_id]

            if (
                strategy.classification.iss_type == "factoring_adjacent"
                and not budget.allow_factoring_adjacent
            ):
                attempts.append(
                    SearchAttempt(
                        strategy_id=strategy.id,
                        status="rejected",
                        reason="strategy_requires_explicit_opt_in",
                        classification=strategy.classification,
                        bounds=BoundsReport(
                            bounded=True,
                            factorization_general=strategy.classification.factorization_general,
                            radius=budget.radius,
                            max_candidates=budget.max_candidates,
                            max_combinations=budget.max_combinations,
                            max_prime_checks=budget.max_prime_checks,
                        ),
                    )
                )
                continue

            attempts.append(strategy.search(n, budget))

        matched = any(attempt.status == "matched" for attempt in attempts)

        return SearchResult(
            kind="structural_payload_search_result",
            input_n=str(n),
            status="matched" if matched else "no_match",
            attempts=attempts,
        )
