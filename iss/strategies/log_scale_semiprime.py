from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from iss.models import (
    BoundsReport,
    PayloadBounds,
    PayloadClassification,
    PayloadStrategy,
    PayloadSupportEntry,
    PayloadVerification,
    SearchAttempt,
    SearchBudget,
    StrategyClassification,
    StructuralPayload,
)
from iss.primes import is_probable_prime, local_prime_candidates
from iss.roots import integer_nth_root_floor
from iss.verify import SupportFactor, verify_support


@dataclass(frozen=True)
class LogScaleSemiprimeStrategy:
    id: str = "log_scale_semiprime"
    classification: StrategyClassification = StrategyClassification(
        iss_type="pure_structural",
        factorization_general=False,
        requires_explicit_opt_in=False,
    )
    max_denominator: int = 8

    def search(self, n: int, budget: SearchBudget) -> SearchAttempt:
        candidates_tested = 0
        prime_checks = 0

        for denominator in range(2, self.max_denominator + 1):
            low_scale = Fraction(1, denominator)
            high_scale = Fraction(denominator - 1, denominator)
            center = integer_nth_root_floor(n, denominator)

            for p in local_prime_candidates(center, budget.radius):
                if candidates_tested >= budget.max_candidates:
                    return self._budget_exhausted(
                        budget=budget,
                        candidates_tested=candidates_tested,
                        prime_checks=prime_checks,
                    )

                candidates_tested += 1
                prime_checks += 1

                if n % p != 0:
                    continue

                q = n // p
                prime_checks += 1

                if not is_probable_prime(q):
                    continue

                verification = verify_support(
                    n,
                    [
                        SupportFactor(base=p, exp=1),
                        SupportFactor(base=q, exp=1),
                    ],
                )

                if not verification.product_equals_input or not verification.prime_checks:
                    continue

                payload = StructuralPayload(
                    kind="structural_payload",
                    input_n=str(n),
                    status="matched",
                    strategy=PayloadStrategy(
                        id=self.id,
                        family="log-scale",
                        profile=[1, 1],
                        scales=[str(low_scale), str(high_scale)],
                        parameters={
                            "radius": budget.radius,
                            "prime_window": True,
                            "max_denominator": self.max_denominator,
                        },
                    ),
                    support=[
                        PayloadSupportEntry(
                            base=str(p),
                            exp=1,
                            role="local_factor",
                            source={
                                "center": str(center),
                                "offset": p - center,
                                "scale": str(low_scale),
                            },
                        ),
                        PayloadSupportEntry(
                            base=str(q),
                            exp=1,
                            role="cofactor",
                            source={
                                "derived_from": f"{n} / {p}",
                                "scale": str(high_scale),
                            },
                        ),
                    ],
                    verification=PayloadVerification(
                        product_equals_input=verification.product_equals_input,
                        prime_checks=verification.prime_checks,
                        reconstructed_product=verification.reconstructed_product,
                    ),
                    bounds=PayloadBounds(
                        bounded=True,
                        factorization_general=False,
                        radius=budget.radius,
                        max_candidates=budget.max_candidates,
                        candidates_tested=candidates_tested,
                        max_prime_checks=budget.max_prime_checks,
                        prime_checks=prime_checks,
                    ),
                    classification=PayloadClassification(
                        iss_type=self.classification.iss_type,
                        factoring_adjacent=False,
                    ),
                )

                return SearchAttempt(
                    strategy_id=self.id,
                    status="matched",
                    reason="found_log_scale_semiprime_payload",
                    classification=self.classification,
                    bounds=BoundsReport(
                        bounded=True,
                        factorization_general=False,
                        radius=budget.radius,
                        max_candidates=budget.max_candidates,
                        candidates_tested=candidates_tested,
                        max_prime_checks=budget.max_prime_checks,
                        prime_checks=prime_checks,
                    ),
                    payloads=[payload],
                )

        return SearchAttempt(
            strategy_id=self.id,
            status="no_match",
            reason="no_dividing_local_prime_found",
            classification=self.classification,
            bounds=BoundsReport(
                bounded=True,
                factorization_general=False,
                radius=budget.radius,
                max_candidates=budget.max_candidates,
                candidates_tested=candidates_tested,
                max_prime_checks=budget.max_prime_checks,
                prime_checks=prime_checks,
            ),
        )

    def _budget_exhausted(
        self,
        budget: SearchBudget,
        candidates_tested: int,
        prime_checks: int,
    ) -> SearchAttempt:
        return SearchAttempt(
            strategy_id=self.id,
            status="budget_exhausted",
            reason="max_candidates_exceeded",
            classification=self.classification,
            bounds=BoundsReport(
                bounded=True,
                factorization_general=False,
                radius=budget.radius,
                max_candidates=budget.max_candidates,
                candidates_tested=candidates_tested,
                max_prime_checks=budget.max_prime_checks,
                prime_checks=prime_checks,
            ),
        )
