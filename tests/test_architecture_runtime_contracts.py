"""Cross-cutting architecture and runtime contract tests."""

from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys
import tomllib


ROOT = Path(__file__).resolve().parents[1]
DOMAIN_ROOT = ROOT / "src" / "autorl" / "domain"


def test_domain_layer_does_not_import_interfaces_or_storage_layers() -> None:
    forbidden_prefixes = (
        "streamlit",
        "fastapi",
        "uvicorn",
        "sqlite3",
        "autorl.interfaces",
        "autorl.infrastructure",
    )
    forbidden_modules = {"argparse"}

    for path in DOMAIN_ROOT.glob("*.py"):
        module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(module):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = alias.name
                    assert imported not in forbidden_modules
                    assert not imported.startswith(forbidden_prefixes)
            if isinstance(node, ast.ImportFrom):
                imported = node.module or ""
                assert imported not in forbidden_modules
                assert not imported.startswith(forbidden_prefixes)


def test_project_targets_python_311_and_documents_virtual_environment_usage() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["requires-python"] == ">=3.11,<3.12"
    assert sys.version_info[:2] == (3, 11)

    operations_manual = (ROOT / "docs" / "operations_manual.md").read_text(encoding="utf-8")
    assert "Python 3.11" in operations_manual
    assert "environment" in operations_manual.lower()


def test_git_repository_is_initialized_for_versioning() -> None:
    assert (ROOT / ".git").exists()
    completed = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "true"
    assert (ROOT / ".gitignore").exists()
