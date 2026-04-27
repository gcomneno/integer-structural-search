from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


StrategyKind = Literal["pure_structural", "factoring_adjacent"]


@dataclass(frozen=True)
class StrategyClassification:
    iss_type: StrategyKind
    factorization_general: bool = False
    requires_explicit_opt_in: bool = False


@dataclass(frozen=True)
class SearchBudget:
    max_candidates: int = 128
    max_combinations: int = 128
    max_prime_checks: int = 128
    radius: int = 16
    allow_factoring_adjacent: bool = False


@dataclass(frozen=True)
class BoundsReport:
    bounded: bool
    factorization_general: bool
    radius: int | None = None
    max_candidates: int | None = None
    candidates_tested: int = 0
    max_combinations: int | None = None
    combinations_tested: int = 0
    max_prime_checks: int | None = None
    prime_checks: int = 0


@dataclass(frozen=True)
class PayloadStrategy:
    id: str
    family: str
    profile: list[int]
    scales: list[str]
    parameters: dict[str, Any]


@dataclass(frozen=True)
class PayloadSupportEntry:
    base: str
    exp: int
    role: str
    source: dict[str, Any]


@dataclass(frozen=True)
class PayloadVerification:
    product_equals_input: bool
    prime_checks: bool
    reconstructed_product: str


@dataclass(frozen=True)
class PayloadBounds:
    bounded: bool
    factorization_general: bool
    radius: int
    max_candidates: int
    candidates_tested: int
    max_prime_checks: int
    prime_checks: int


@dataclass(frozen=True)
class PayloadClassification:
    iss_type: StrategyKind
    factoring_adjacent: bool


@dataclass(frozen=True)
class StructuralPayload:
    kind: str
    input_n: str
    status: Literal["matched"]
    strategy: PayloadStrategy
    support: list[PayloadSupportEntry]
    verification: PayloadVerification
    bounds: PayloadBounds
    classification: PayloadClassification

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchAttempt:
    strategy_id: str
    status: Literal["matched", "no_match", "budget_exhausted", "rejected"]
    reason: str
    classification: StrategyClassification
    bounds: BoundsReport
    payloads: list[dict[str, Any]] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchResult:
    kind: str
    input_n: str
    status: Literal["matched", "no_match"]
    attempts: list[SearchAttempt]

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        matched_attempts = [
            attempt
            for attempt in self.attempts
            if attempt.status == "matched"
        ]

        data["summary"] = {
            "matched": self.status == "matched",
            "strategies_attempted": len(self.attempts),
            "matches_count": len(matched_attempts),
            "matched_strategy_ids": [
                attempt.strategy_id
                for attempt in matched_attempts
            ],
            "factorization_general": any(
                attempt.classification.factorization_general
                for attempt in self.attempts
            ),
        }
        return data
