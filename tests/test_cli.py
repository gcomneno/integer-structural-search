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
    assert data["attempts"][0]["strategy_id"] == "log_scale_semiprime"

    payload = data["attempts"][0]["payloads"][0]
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


def test_cli_rejects_invalid_input() -> None:
    result = run_cli("1")

    assert result.returncode != 0
    assert "greater than 1" in result.stderr
