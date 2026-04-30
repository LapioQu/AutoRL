"""Configuration loading and validation helpers for phase 1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

import yaml

from autorl.domain.errors import ConfigValidationError
from autorl.domain.models import Config


def load_config(path: str | Path) -> Config:
    """Load and validate a YAML or JSON experiment configuration."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"configuration file does not exist: {file_path}")
    if file_path.suffix.lower() not in {".yaml", ".yml", ".json"}:
        raise ConfigValidationError(f"unsupported config format: {file_path.suffix}")

    raw_text = file_path.read_text(encoding="utf-8")
    raw_data = _parse_payload(raw_text, file_path.suffix.lower())
    return load_config_from_mapping(raw_data)


def load_config_from_mapping(data: Mapping[str, Any]) -> Config:
    """Build a validated Config from an in-memory mapping."""
    return Config.from_dict(data)


def _parse_payload(raw_text: str, suffix: str) -> Mapping[str, Any]:
    if suffix == ".json":
        data = json.loads(raw_text)
    else:
        data = yaml.safe_load(raw_text)

    if not isinstance(data, Mapping):
        raise ConfigValidationError("configuration root must be a mapping")
    return data
