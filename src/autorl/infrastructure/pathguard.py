"""Filesystem path guard for artifact writes."""

from __future__ import annotations

from pathlib import Path
import shutil

from autorl.domain.errors import ConfigValidationError


class PathGuard:
    """Restrict writes to a configured root directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve_relative(self, relative_path: str | Path) -> Path:
        candidate = Path(relative_path)
        resolved = candidate.resolve() if candidate.is_absolute() else (self.root / candidate).resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise ConfigValidationError(f"path escapes artifacts root: {relative_path}")
        return resolved

    def ensure_directory(self, relative_path: str | Path = ".") -> Path:
        path = self.resolve_relative(relative_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_text(self, relative_path: str | Path, content: str, *, encoding: str = "utf-8") -> Path:
        path = self.resolve_relative(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)
        return path

    def append_text(self, relative_path: str | Path, content: str, *, encoding: str = "utf-8") -> Path:
        path = self.resolve_relative(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding=encoding, newline="") as handle:
            handle.write(content)
        return path

    def write_bytes(self, relative_path: str | Path, content: bytes) -> Path:
        path = self.resolve_relative(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def copy_file(self, source_path: str | Path, relative_destination: str | Path) -> Path:
        destination = self.resolve_relative(relative_destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(source_path), destination)
        return destination
