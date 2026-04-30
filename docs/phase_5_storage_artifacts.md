# Phase 5: storage, logs, and artifacts

Phase 5 adds the reproducibility and traceability layer: guarded filesystem artifacts plus SQLite-backed persistence.

## Implemented scope

- `PathGuard` to restrict writes to the configured artifacts root;
- `SQLiteRepository` with tables for:
  - `experiments`
  - `configs`
  - `episode_metrics`
  - `window_metrics`
  - `decisions`
  - `artifacts`
  - `events`
- `ExperimentArtifactStore` for:
  - `config.yaml`
  - `config_hash.txt`
  - `versions.json`
  - `metrics.csv`
  - `window_metrics.csv`
  - `decisions.csv`
  - `events.log`

## Reproducibility behavior

- every experiment bundle stores config snapshot, seed-linked experiment record, config hash, package versions, metrics, decisions, and artifact paths;
- SQLite and filesystem outputs are written together for round-trip traceability;
- artifact writes outside the configured root are blocked by `PathGuard`.

## Error handling

- event logs are appended incrementally;
- failed artifact writes emit an `ERROR` event and preserve prior log lines;
- integration tests verify partial log retention after a guarded write failure.
