"""Phase 0 smoke tests."""

from __future__ import annotations

import importlib
import subprocess
import sys

import autorl
import pytest
from autorl.bootstrap import import_check


def test_package_import_exposes_version() -> None:
    assert autorl.__version__ == "0.1.0"


def test_import_check_message_is_stable() -> None:
    assert import_check() == "AutoRL package import OK"


@pytest.mark.parametrize(
    "module_name",
    [
        "autorl.application",
        "autorl.application.benchmark_replay",
        "autorl.application.experiments",
        "autorl.application.reporting",
        "autorl.application.validation",
        "autorl.domain",
        "autorl.domain.environment",
        "autorl.domain.evaluation",
        "autorl.domain.metacontroller",
        "autorl.domain.metrics",
        "autorl.domain.strategy_runtime",
        "autorl.infrastructure.artifacts",
        "autorl.infrastructure.pathguard",
        "autorl.infrastructure.repository",
        "autorl.infrastructure",
        "autorl.interfaces",
        "autorl.interfaces.api",
        "autorl.interfaces.cli",
        "autorl.interfaces.cli.app",
        "autorl.interfaces.ui",
    ],
)
def test_phase_0_scaffold_modules_import(module_name: str) -> None:
    assert importlib.import_module(module_name) is not None


def test_module_entrypoint_runs_successfully() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "autorl"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "AutoRL package import OK" in completed.stdout
