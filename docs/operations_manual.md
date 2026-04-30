# Operations Manual

## Purpose

This manual defines the operational workflow for the AutoRL system in the final diploma scope.

## Environment

- Operating system: Windows or Linux
- Python 3.11 runtime
- Package mode: editable install
- Main workspace: repository root

## Installation

```bash
python -m pip install -e .[dev]
```

## Import Smoke

```bash
python -m autorl
```

Expected result:
- `AutoRL package import OK`

## Core CLI Workflow

Validate configuration:

```bash
python -m autorl validate-config --config configs/examples/stationary.yaml
```

Run experiment:

```bash
python -m autorl run --config configs/examples/stationary.yaml
```

List experiments:

```bash
python -m autorl list
```

Read experiment status:

```bash
python -m autorl status --experiment-id EXP_ID --artifacts-root artifacts
```

Read experiment report:

```bash
python -m autorl report --experiment-id EXP_ID --artifacts-root artifacts
```

Rerun experiment:

```bash
python -m autorl rerun --experiment-id EXP_ID --artifacts-root artifacts
```

Export experiment:

```bash
python -m autorl export --experiment-id EXP_ID --artifacts-root artifacts --format zip
```

## Validation and Benchmark CLI

Validation suite:

```bash
python -m autorl validate-suite --artifacts-root artifacts/validation_suite_0_7
```

Single benchmark:

```bash
python -m autorl benchmark-elec2 --artifacts-root artifacts/real_stream_validation/elec2 --max-samples 256
```

Benchmark suite:

```bash
python -m autorl benchmark-suite --artifacts-root artifacts/real_stream_validation/suite --datasets elec2 --max-samples 256
```

Phase 10 smoke:

```bash
python -m autorl phase10-suite --artifacts-root artifacts/phase10_experimental_series --series E1 --benchmark-datasets elec2 --benchmark-max-samples 128
```

## API Operation

Start backend:

```bash
uvicorn autorl.interfaces.api.app:create_app --factory --reload
```

Primary endpoints:
- `GET /health`
- `GET /scenarios`
- `GET /strategies`
- `POST /experiments`
- `POST /experiments/{id}/start`
- `GET /experiments/{id}/status`
- `GET /experiments/{id}/metrics`
- `GET /experiments/{id}/decisions`
- `GET /experiments/{id}/report`
- `POST /experiments/{id}/rerun`
- `POST /experiments/{id}/stop`
- `GET /compare`

## UI Operation

Start UI:

```bash
streamlit run src/autorl/interfaces/ui/app.py
```

Main product flow:
1. Open `Forecast Studio`.
2. Load a built-in dataset or upload a CSV file.
3. Run analysis.
4. Monitor execution.
5. Review results in reports and evidence views.

## Artifact Layout

Typical experiment artifact set:
- `config.yaml`
- `config_hash.txt`
- `versions.json`
- `metrics.csv`
- `window_metrics.csv`
- `decisions.csv`
- `events.log`
- `report.md`
- `report.html`
- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

Benchmark replay artifact set:
- `summary.json`
- `summary.md`
- `decisions.csv`

## Export Formats

Supported export formats:
- `json`
- `markdown`
- `html`
- `zip`

## Privacy Rules

- Uploaded datasets must not be persisted as raw user files unless the workflow explicitly requires it.
- Dataset Lab persistence should prefer manifests, hashes, schema summaries, and derived artifacts.

## Monitoring and Recovery

- Use `status` and `report` commands for CLI workflows.
- Use API endpoints for service monitoring.
- Use the UI monitor for live experiment progress.
- If an experiment fails, inspect:
  - `events.log`
  - `decisions.csv`
  - `report.md`

## Final Verification References

- `docs/requirements_inventory.md`
- `docs/requirements_traceability.md`
- `docs/test_protocol.md`
