# Phase 6: experiment orchestrator and CLI

Phase 6 turns the previously isolated domain and infrastructure layers into the first real end-to-end execution path.

## Implemented scope

- `ExperimentOrchestrator` in `autorl.application.experiments`
- end-to-end run from config to:
  - experiment bundle creation
  - strategy simulation
  - adaptive Stay/Switch selection
  - persisted `metrics.csv`
  - persisted `window_metrics.csv`
  - persisted `decisions.csv`
  - persisted `events.log`
- CLI commands:
  - `autorl run --config ...`
  - `autorl list`
  - `autorl report --experiment-id ...`
  - `autorl rerun --experiment-id ...`

## Orchestration model

- every enabled strategy is simulated against the same seed-controlled environment;
- rolling window metrics are computed per strategy;
- the metacontroller compares the current strategy against the strongest available candidate at each evaluation point;
- the managed run is composed from the selected strategy trajectory and persisted as the canonical experiment result.

## Verification

- e2e run test for `stationary`
- e2e run test for `abrupt_drift`
- reproducibility test for repeated runs with the same seed
- CLI smoke tests for `run`, `list`, `report`, and `rerun`
