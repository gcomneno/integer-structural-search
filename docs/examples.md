# ISS Examples

Worked examples for Integer Structural Search / ISS.

These examples show how ISS behaves with the current default strategy set:

- `balanced_root_scale_semiprime`
- `log_scale_semiprime`

ISS is a bounded structural search engine.

It does not claim to factor arbitrary integers.

It tries declared, bounded strategies and either returns verified structural payloads or clean failures.

---

## 1. Balanced semiprime with default strategies

Input:

    100160063 = 10007 * 10009

Command:

    python -m iss.cli 100160063 --radius 2

Expected behavior:

- `balanced_root_scale_semiprime` matches;
- `log_scale_semiprime` also matches;
- `matches_count` is `2`.

Why both match:

- the number is balanced;
- the balanced strategy searches near `sqrt(n)`;
- the log-scale strategy includes the scale split `[1/2, 1/2]`.

Interpretation:

    Two structural strategies found the same valid support.

This is expected.

ISS currently does not deduplicate equivalent payloads.

Relevant summary:

    "summary": {
      "factorization_general": false,
      "matched": true,
      "matched_strategy_ids": [
        "balanced_root_scale_semiprime",
        "log_scale_semiprime"
      ],
      "matches_count": 2,
      "strategies_attempted": 2
    }

Structural support found:

    10007 * 10009 == 100160063

---

## 2. Balanced semiprime with strategy selection

Input:

    100160063 = 10007 * 10009

Command:

    python -m iss.cli 100160063 --radius 2 --strategy balanced_root_scale_semiprime

Expected behavior:

- only `balanced_root_scale_semiprime` runs;
- the result is `matched`;
- `strategies_attempted` is `1`;
- `matches_count` is `1`.

Useful when testing one strategy in isolation.

Expected matched strategy:

    balanced_root_scale_semiprime

Expected support:

    10007
    10009

---

## 3. Unbalanced semiprime with default strategies

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001

Expected behavior:

- `balanced_root_scale_semiprime` fails cleanly;
- `log_scale_semiprime` matches;
- `matches_count` is `1`.

Why balanced root-scale fails:

    sqrt(3465924001) is around 58872

The actual small factor is:

    71

So the small factor is far outside the balanced root window.

Why log-scale succeeds:

The log-scale strategy tries scale splits such as:

    [1/2, 1/2]
    [1/3, 2/3]
    [1/4, 3/4]
    [1/5, 4/5]

For the split:

    [1/5, 4/5]

the low center is near:

    3465924001^(1/5) ≈ 80

With radius `16`, the candidate window includes:

    71

ISS then verifies:

    71 * 48815831 == 3465924001

Relevant summary:

    "summary": {
      "factorization_general": false,
      "matched": true,
      "matched_strategy_ids": [
        "log_scale_semiprime"
      ],
      "matches_count": 1,
      "strategies_attempted": 2
    }

---

## 4. Unbalanced semiprime with log-scale only

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001 --strategy log_scale_semiprime

Expected behavior:

- only `log_scale_semiprime` runs;
- the result is `matched`;
- `strategies_attempted` is `1`;
- `matches_count` is `1`.

Expected matched strategy:

    log_scale_semiprime

Expected structural scale:

    [1/5, 4/5]

Expected support:

    71
    48815831

---

## 5. Radius sensitivity: failure

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001 --radius 4 --strategy log_scale_semiprime

Expected behavior:

- `log_scale_semiprime` fails cleanly;
- result status is `no_match`;
- `matches_count` is `0`;
- `payloads` is empty.

Why:

The useful low center is near:

    80

The target factor is:

    71

Offset:

    -9

With radius `4`, the local window does not include `71`.

Expected reason:

    no_dividing_local_prime_found

Important interpretation:

    This is not a correctness failure.
    It means no candidate was found within the declared bounded window.

---

## 6. Radius sensitivity: success

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001 --radius 16 --strategy log_scale_semiprime

Expected behavior:

- `log_scale_semiprime` matches;
- result status is `matched`;
- `matches_count` is `1`.

Why:

The low center is near:

    80

The factor is:

    71

Offset:

    -9

With radius `16`, the local window includes `71`.

Expected support:

    71
    48815831

Expected verification:

    product_equals_input: true
    prime_checks: true

---

## 7. Candidate budget sensitivity: exhausted budget

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001 --max-candidates 1 --strategy log_scale_semiprime

Expected behavior:

- result status is `no_match`;
- attempt status is `budget_exhausted`;
- reason is `max_candidates_exceeded`;
- `matches_count` is `0`;
- `payloads` is empty.

Interpretation:

    The declared candidate budget was not enough to reach a valid structural candidate.

---

## 8. Candidate budget sensitivity: enough budget

Input:

    3465924001 = 71 * 48815831

Command:

    python -m iss.cli 3465924001 --max-candidates 32 --strategy log_scale_semiprime

Expected behavior:

- `log_scale_semiprime` matches;
- result status is `matched`;
- `matches_count` is `1`.

Observed useful values:

    candidates_tested: 12
    prime_checks: 13

Expected support:

    71
    48815831

Expected verification:

    product_equals_input: true
    prime_checks: true

---

## 9. Number outside current strategy coverage

Input:

    100000002790000029250000142519000317757090255987171

Known context:

- 51 digits;
- squarefree k5-style structure;
- not a semiprime profile `[1, 1]`.

Command:

    python -m iss.cli 100000002790000029250000142519000317757090255987171

Expected behavior with the current default strategies:

- `balanced_root_scale_semiprime` returns `no_match`;
- `log_scale_semiprime` returns `no_match`;
- result status is `no_match`;
- `matches_count` is `0`;
- `payloads` is empty.

Interpretation:

    ISS does not invent a semiprime payload for a number outside the active strategy coverage.

This is correct.

Current strategies target semiprime profile:

    [1, 1]

They should not claim a k5 payload.

---

## 10. Useful filtering commands

Show strategy ids, statuses, reasons, scales and bases:

    python -m iss.cli 3465924001 | python -m json.tool | rg -n '"strategy_id"|"status"|"reason"|"base"|"scales"'

Show multi-match summary:

    python -m iss.cli 100160063 --radius 2 | python -m json.tool | tail -25

Show only the log-scale strategy on the unbalanced case:

    python -m iss.cli 3465924001 --strategy log_scale_semiprime | python -m json.tool | rg -n '"strategy_id"|"status"|"base"'

Show only the balanced strategy on the balanced case:

    python -m iss.cli 100160063 --radius 2 --strategy balanced_root_scale_semiprime | python -m json.tool | rg -n '"strategy_id"|"status"|"base"'

---

## Summary of current behavior

Current good behavior:

- balanced semiprime can produce two valid matches;
- unbalanced semiprime is found by log-scale;
- too-small radius produces clean `no_match`;
- insufficient budget produces `budget_exhausted`;
- unsupported k5-style input produces clean `no_match`;
- all matches report `factorization_general: false`;
- multi-match behavior is observable through summary fields.
