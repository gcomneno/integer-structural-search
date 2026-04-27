from __future__ import annotations

import argparse
import json

from iss.engine import StructuralSearchEngine
from iss.models import SearchBudget
from iss.registry import StrategyRegistry
from iss.strategies.balanced_root_scale import BalancedRootScaleSemiprimeStrategy
from iss.strategies.log_scale_semiprime import LogScaleSemiprimeStrategy


def build_default_engine() -> StructuralSearchEngine:
    registry = StrategyRegistry()
    registry.register(BalancedRootScaleSemiprimeStrategy())
    registry.register(LogScaleSemiprimeStrategy())
    return StructuralSearchEngine.from_registry(registry)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iss",
        description="Integer Structural Search: bounded structural search over integers.",
    )
    parser.add_argument("n", type=int, help="Input integer greater than 1")
    parser.add_argument("--radius", type=int, default=16)
    parser.add_argument("--max-candidates", type=int, default=128)
    parser.add_argument(
        "--allow-factoring-adjacent",
        action="store_true",
        help="Allow explicitly registered factoring-adjacent strategies.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    engine = build_default_engine()

    try:
        result = engine.search(
            args.n,
            budget=SearchBudget(
                radius=args.radius,
                max_candidates=args.max_candidates,
                allow_factoring_adjacent=args.allow_factoring_adjacent,
            ),
        )
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(result.to_json_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
