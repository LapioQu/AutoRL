# AutoRL Strategy Manager

Local adaptive system for strategy switching, non-stationary validation, benchmark replay, and product-style forecasting workflows.

## Scope

The project includes:
- modular monolith architecture: `domain / application / infrastructure / interfaces`
- orchestrated experiments with persisted artifacts
- utility + LCB based switching
- CLI, FastAPI, and Streamlit interfaces
- validation suites and benchmark replay
- Phase 10 experimental series artifacts
- Phase 11 traceability and documentation package

## Primary References

- `docs/requirements_inventory.md`
- `docs/requirements_traceability.md`
- `docs/test_protocol.md`
- `docs/operations_manual.md`
- `docs/phase_10_experimental_series.md`

## Quick Start

Recommended runtime: Python `3.11`.

```bash
python -m pip install -e .[dev]
python -m autorl
python -m pytest -q
uvicorn autorl.interfaces.api.app:create_app --factory --reload
streamlit run src/autorl/interfaces/ui/app.py
```

## Core CLI

Validate config:

```bash
python -m autorl validate-config --config configs/examples/stationary.yaml
```

Run one experiment:

```bash
python -m autorl run --config configs/examples/stationary.yaml
```

List experiments:

```bash
python -m autorl list
```

Read status:

```bash
python -m autorl status --experiment-id EXP_ID --artifacts-root artifacts
```

Read report:

```bash
python -m autorl report --experiment-id EXP_ID --artifacts-root artifacts
```

Export artifacts:

```bash
python -m autorl export --experiment-id EXP_ID --artifacts-root artifacts --format zip
```

## API and UI

Start backend:

```bash
uvicorn autorl.interfaces.api.app:create_app --factory --reload
```

Start UI:

```bash
streamlit run src/autorl/interfaces/ui/app.py
```

## Benchmark and Validation

Validation suite:

```bash
python -m autorl validate-suite --artifacts-root artifacts/validation_suite_0_7
```

Single benchmark:

```bash
python -m autorl benchmark-elec2 --artifacts-root artifacts/real_stream_validation/elec2 --max-samples 256
```

Suite benchmark:

```bash
python -m autorl benchmark-suite --artifacts-root artifacts/real_stream_validation/suite --datasets elec2 --max-samples 256
```

Phase 10 smoke:

```bash
python -m autorl phase10-suite --artifacts-root artifacts/phase10_experimental_series --series E1 --benchmark-datasets elec2 --benchmark-max-samples 128
```

## Repository Layout

```text
src/
  autorl/
    application/
    domain/
    infrastructure/
    interfaces/
      api/
      cli/
      ui/
tests/
docs/
artifacts/
```

## Final Verification

Use:

```bash
python -m autorl
python -m pytest -q
```

For the formal verification flow, see `docs/test_protocol.md`.
