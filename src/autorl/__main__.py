"""CLI entry point for import checks and phase 6 commands."""

from __future__ import annotations

import sys

from autorl.bootstrap import import_check
from autorl.interfaces.cli import run_cli


def main(argv: list[str] | None = None) -> int:
    """Run the default import check or the phase 6 CLI."""
    actual_argv = sys.argv[1:] if argv is None else argv
    if not actual_argv:
        message = import_check()
        print(message)
        return 0
    return run_cli(actual_argv)


if __name__ == "__main__":
    raise SystemExit(main())
