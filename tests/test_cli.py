from __future__ import annotations

import json
import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "iss.cli", *args],
        check=False,
        text=True,
        capture_output=True,
    )


def test_cli_finds_log_scale_semiprime_payload() -> None:
    result = run_cli("3465924001")

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "matched"
    assert data["input_n"] == "3465924001"

    matched_attempts = [
        attempt
        for attempt in data["attempts"]
        if attempt["status"] == "matched"
    ]

    assert len(matched_attempts) == 1
    assert matched_attempts[0]["strategy_id"] == "log_scale_semiprime"

    payload = matched_attempts[0]["payloads"][0]
    assert payload["support"][0]["base"] == "71"
    assert payload["support"][1]["base"] == "48815831"
    assert payload["verification"]["product_equals_input"] is True
    assert payload["verification"]["prime_checks"] is True


def test_cli_radius_too_small_fails_cleanly() -> None:
    result = run_cli("3465924001", "--radius", "4")

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "no_match"
    assert data["attempts"][0]["status"] == "no_match"
    assert data["attempts"][0]["reason"] == "no_dividing_local_prime_found"


def test_cli_rejects_invalid_input_without_traceback() -> None:
    result = run_cli("1")

    assert result.returncode == 2
    assert "ISS input must be an integer greater than 1" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""


def test_cli_finds_balanced_root_scale_semiprime_payload() -> None:
    result = run_cli(str(10007 * 10009), "--radius", "2")

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "matched"

    matched_attempts = [
        attempt
        for attempt in data["attempts"]
        if attempt["status"] == "matched"
    ]

    balanced_matches = [
        attempt
        for attempt in matched_attempts
        if attempt["strategy_id"] == "balanced_root_scale_semiprime"
    ]

    assert len(balanced_matches) == 1

    payload = balanced_matches[0]["payloads"][0]
    assert payload["support"][0]["base"] == "10007"
    assert payload["support"][1]["base"] == "10009"
    assert payload["verification"]["product_equals_input"] is True


def test_cli_can_select_log_scale_strategy_only() -> None:
    result = run_cli(
        "3465924001",
        "--strategy",
        "log_scale_semiprime",
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "matched"
    assert [attempt["strategy_id"] for attempt in data["attempts"]] == [
        "log_scale_semiprime"
    ]


def test_cli_can_select_balanced_strategy_only() -> None:
    result = run_cli(
        str(10007 * 10009),
        "--radius",
        "2",
        "--strategy",
        "balanced_root_scale_semiprime",
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "matched"
    assert [attempt["strategy_id"] for attempt in data["attempts"]] == [
        "balanced_root_scale_semiprime"
    ]


def test_cli_can_select_multiple_strategies() -> None:
    result = run_cli(
        str(10007 * 10009),
        "--radius",
        "2",
        "--strategy",
        "balanced_root_scale_semiprime",
        "--strategy",
        "log_scale_semiprime",
    )

    assert result.returncode == 0
    data = json.loads(result.stdout)

    assert data["status"] == "matched"
    assert [attempt["strategy_id"] for attempt in data["attempts"]] == [
        "balanced_root_scale_semiprime",
        "log_scale_semiprime",
    ]
