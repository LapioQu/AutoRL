# Phase 1: domain models and configurations

Phase 1 establishes the formal configuration contract without introducing runtime orchestration, RL environment behavior, or API/UI execution paths.

## Implemented scope

- immutable domain entities: `Experiment`, `Config`, `LearningStrategy`, `EpisodeMetric`, `WindowMetric`, `Decision`, `Artifact`;
- typed enums for scenario names, run modes, decision actions, and artifact kinds;
- YAML/JSON config loading via `autorl.application.configs.load_config`;
- validation rules for supported scenarios and metacontroller thresholds;
- stable `config_hash` derived from canonical JSON serialization;
- example configs for `stationary`, `abrupt_drift`, `gradual_drift`, `noisy_reward`, `fallback`, and `reproducibility`.

## Deliberate limits

Phase 1 does not implement:

- RL environment transitions or reward generation;
- learning strategy execution logic;
- Stay/Switch evaluation formulas;
- persistence, artifacts storage, or experiment orchestration;
- FastAPI endpoints or Streamlit pages.

## Validation principles

- config roots must be mappings loaded from `.yaml`, `.yml`, or `.json`;
- strategy names must be unique and at least one strategy must remain enabled;
- `meta_controller.min_samples` must not exceed `meta_controller.window_size`;
- scenario-specific fields are validated per scenario type;
- `config_hash` is stable for semantically identical payloads independent of mapping key order.
