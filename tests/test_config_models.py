"""Phase 1 tests for configuration models and validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from autorl.application import load_config, load_config_from_mapping
from autorl.domain import ConfigValidationError, RunMode, ScenarioName


EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "configs" / "examples"


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "file_name, expected_scenario",
    [
        ("stationary.yaml", ScenarioName.STATIONARY),
        ("abrupt_drift.yaml", ScenarioName.ABRUPT_DRIFT),
        ("gradual_drift.yaml", ScenarioName.GRADUAL_DRIFT),
        ("noisy_reward.yaml", ScenarioName.NOISY_REWARD),
        ("fallback.yaml", ScenarioName.FALLBACK),
        ("reproducibility.json", ScenarioName.REPRODUCIBILITY),
    ],
)
def test_example_configs_load_successfully(file_name: str, expected_scenario: ScenarioName) -> None:
    config = load_config(EXAMPLES_DIR / file_name)

    assert config.scenario.name is expected_scenario
    assert config.mode is RunMode.ADAPTIVE
    assert config.config_hash
    assert len(config.strategies) >= 1


def test_config_hash_is_stable_for_same_payload_with_different_key_order() -> None:
    source = _read_yaml(EXAMPLES_DIR / "stationary.yaml")
    reordered = {
        "notes": source["notes"],
        "tags": source["tags"],
        "artifacts_root": source["artifacts_root"],
        "meta_controller": {
            "utility_weights": {
                "switch_cost": source["meta_controller"]["utility_weights"]["switch_cost"],
                "compute_cost": source["meta_controller"]["utility_weights"]["compute_cost"],
                "reward_variance": source["meta_controller"]["utility_weights"]["reward_variance"],
                "reward_mean": source["meta_controller"]["utility_weights"]["reward_mean"],
            },
            "switch_cost": source["meta_controller"]["switch_cost"],
            "lambda": source["meta_controller"]["lambda"],
            "delta": source["meta_controller"]["delta"],
            "min_samples": source["meta_controller"]["min_samples"],
            "window_size": source["meta_controller"]["window_size"],
        },
        "strategies": [
            {
                "compute_cost": source["strategies"][0]["compute_cost"],
                "parameters": source["strategies"][0]["parameters"],
                "name": source["strategies"][0]["name"],
            },
            {
                "description": source["strategies"][1].get("description"),
                "compute_cost": source["strategies"][1]["compute_cost"],
                "parameters": source["strategies"][1]["parameters"],
                "enabled": source["strategies"][1].get("enabled", True),
                "name": source["strategies"][1]["name"],
            },
        ],
        "scenario": {
            "description": source["scenario"]["description"],
            "tags": source["scenario"]["tags"],
            "steps_per_episode": source["scenario"]["steps_per_episode"],
            "episodes": source["scenario"]["episodes"],
            "name": source["scenario"]["name"],
        },
        "mode": source["mode"],
        "seed": source["seed"],
        "experiment_name": source["experiment_name"],
        "schema_version": source["schema_version"],
    }

    config_a = load_config_from_mapping(source)
    config_b = load_config_from_mapping(reordered)

    assert config_a.to_dict() == config_b.to_dict()
    assert config_a.config_hash == config_b.config_hash


def test_config_hash_changes_when_payload_changes() -> None:
    source = _read_yaml(EXAMPLES_DIR / "stationary.yaml")
    changed = dict(source)
    changed["seed"] = source["seed"] + 1

    config_a = load_config_from_mapping(source)
    config_b = load_config_from_mapping(changed)

    assert config_a.config_hash != config_b.config_hash


def test_invalid_config_rejects_unknown_scenario(tmp_path: Path) -> None:
    invalid = _read_yaml(EXAMPLES_DIR / "stationary.yaml")
    invalid["scenario"]["name"] = "unknown_mode"
    path = tmp_path / "invalid.yaml"
    path.write_text(yaml.safe_dump(invalid, sort_keys=False), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="unsupported scenario.name"):
        load_config(path)


def test_invalid_config_rejects_duplicate_strategy_names(tmp_path: Path) -> None:
    invalid = _read_yaml(EXAMPLES_DIR / "stationary.yaml")
    invalid["strategies"][1]["name"] = invalid["strategies"][0]["name"]
    path = tmp_path / "duplicate.yaml"
    path.write_text(yaml.safe_dump(invalid, sort_keys=False), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="strategy names must be unique"):
        load_config(path)


def test_invalid_config_rejects_gradual_drift_without_end(tmp_path: Path) -> None:
    invalid = _read_yaml(EXAMPLES_DIR / "gradual_drift.yaml")
    invalid["scenario"].pop("drift_end_episode")
    path = tmp_path / "gradual-invalid.yaml"
    path.write_text(yaml.safe_dump(invalid, sort_keys=False), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="gradual_drift scenario requires"):
        load_config(path)


def test_invalid_config_rejects_min_samples_above_window_size(tmp_path: Path) -> None:
    invalid = json.loads((EXAMPLES_DIR / "reproducibility.json").read_text(encoding="utf-8"))
    invalid["meta_controller"]["min_samples"] = invalid["meta_controller"]["window_size"] + 1
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(invalid), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="min_samples must be <="):
        load_config(path)
