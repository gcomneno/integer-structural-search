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
