from __future__ import annotations

from iss.engine import StructuralStrategy


class StrategyRegistry:
    def __init__(self) -> None:
        self._strategies: dict[str, StructuralStrategy] = {}

    def register(self, strategy: StructuralStrategy) -> None:
        if strategy.id in self._strategies:
            raise ValueError(f"Strategy already registered: {strategy.id}")

        self._strategies[strategy.id] = strategy

    def get(self, strategy_id: str) -> StructuralStrategy:
        try:
            return self._strategies[strategy_id]
        except KeyError as exc:
            raise KeyError(f"Unknown strategy: {strategy_id}") from exc

    def all(self) -> list[StructuralStrategy]:
        return list(self._strategies.values())

    def ids(self) -> list[str]:
        return sorted(self._strategies)
