# Integer Structural Search / ISS

ISS is a bounded structural search engine for integer payloads.

It is intentionally separated from PET / artifact reconstruction.

ISS does **not** claim to factor arbitrary large integers.

It tries declared, bounded, structural strategies and either returns verified structural payloads or clean failures.

## Core promise

ISS promises:

- declared strategies;
- explicit bounds;
- stable JSON output;
- verified product reconstruction when a match is found;
- clean `no_match` results when no bounded structural candidate is found.

ISS does **not** promise:

- general integer factorization;
- reconstruction of arbitrary opaque numbers;
- hidden unbounded search;
- "miracle" decomposition of large integers without structural assumptions.

## Search layer vs verification layer

ISS separates two concerns.

### Search layer

The search layer generates candidates from declared structural assumptions.

Example:

```text
profile = [1, 1]
scale = [1/5, 4/5]
center = floor(n^(1/5))
radius = 16
```

## Multi-match behavior

ISS may return more than one successful attempt for the same input.

This can happen when different pure structural strategies discover the same valid support.

Example:

```text
100160063 = 10007 * 10009

With the default strategy set and a small radius, both strategies may match:

balanced_root_scale_semiprime
log_scale_semiprime

This is expected.

The summary reports this explicitly:

{
  "summary": {
    "matched": true,
    "strategies_attempted": 2,
    "matches_count": 2,
    "matched_strategy_ids": [
      "balanced_root_scale_semiprime",
      "log_scale_semiprime"
    ],
    "factorization_general": false
  }
}

ISS currently does not deduplicate equivalent payloads.

This is intentional.

Different strategies reaching the same support are useful evidence during structural probing.

Deduplication or best-match selection may be added later as an explicit policy layer.

## CLI strategy selection

By default, the ISS CLI runs all registered default strategies.

Current default strategies:

- `balanced_root_scale_semiprime`
- `log_scale_semiprime`

Run all default strategies:

    python -m iss.cli 100160063 --radius 2

Run only the balanced root-scale strategy:

    python -m iss.cli 100160063 --radius 2 --strategy balanced_root_scale_semiprime

Run only the log-scale semiprime strategy:

    python -m iss.cli 3465924001 --strategy log_scale_semiprime

The `--strategy` option can be repeated:

    python -m iss.cli 100160063 --radius 2 \
      --strategy balanced_root_scale_semiprime \
      --strategy log_scale_semiprime

When no `--strategy` option is provided, all registered default strategies are attempted in registry order.

Strategy selection does not change ISS semantics.

It only limits which declared strategies are run for that invocation.
