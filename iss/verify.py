from __future__ import annotations

from dataclasses import asdict, dataclass

from iss.primes import is_probable_prime


@dataclass(frozen=True)
class SupportFactor:
    base: int
    exp: int


@dataclass(frozen=True)
class VerificationReport:
    product_equals_input: bool
    prime_checks: bool
    reconstructed_product: str

    def to_json_dict(self) -> dict[str, object]:
        return asdict(self)


def verify_support(n: int, support: list[SupportFactor]) -> VerificationReport:
    product = 1

    for item in support:
        product *= item.base**item.exp

    return VerificationReport(
        product_equals_input=product == n,
        prime_checks=all(is_probable_prime(item.base) for item in support),
        reconstructed_product=str(product),
    )
