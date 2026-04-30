"""Bootstrap helpers that are safe to keep minimal in phase 0."""


def import_check() -> str:
    """Return a stable message when the package imports correctly."""
    return "AutoRL package import OK"
