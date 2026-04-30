# Test Protocol

## Purpose

This protocol defines the final verification flow for the AutoRL diploma project in Phase 11.

## Verification Layers

1. Import and packaging smoke
2. Unit and integration tests
3. CLI smoke
4. API smoke
5. UI smoke
6. Validation and benchmark artifacts
7. Performance and memory checks
8. Documentation completeness checks

## Canonical Commands

### Import Smoke

```bash
python -m autorl
```

Expected result:
- `AutoRL package import OK`

### Full pytest Regression

Preferred command:

```bash
python -m pytest -q
```

If runtime is too high, split into batches:

```bash
python -m pytest tests/test_ai_review.py tests/test_api_fastapi.py tests/test_architecture_runtime_contracts.py tests/test_benchmark_profiles.py tests/test_benchmark_replay.py tests/test_config_models.py -q
python -m pytest tests/test_dataset_lab.py tests/test_environment.py tests/test_evaluator_metacontroller.py tests/test_imports.py tests/test_orchestrator_cli.py tests/test_state_and_exports.py -q
python -m pytest tests/test_storage_and_artifacts.py tests/test_strategies_and_metrics.py tests/test_ui_streamlit.py tests/test_validation_suite.py tests/test_phase10_suite.py tests/test_phase11_docs.py -q
```

Expected result:
- all batches pass

### Coverage Check

```bash
python -m pytest --cov=src/autorl --cov-report=term-missing -q
```

Expected result:
- tests pass
- coverage report is generated

## CLI Smoke Matrix

Run at least the following commands:

```bash
python -m autorl validate-config --config configs/examples/stationary.yaml
python -m autorl run --config configs/examples/stationary.yaml
python -m autorl list
python -m autorl report --experiment-id EXP_ID --artifacts-root artifacts
python -m autorl rerun --experiment-id EXP_ID --artifacts-root artifacts
python -m autorl status --experiment-id EXP_ID --artifacts-root artifacts
python -m autorl export --experiment-id EXP_ID --artifacts-root artifacts --format zip
python -m autorl benchmark-elec2 --artifacts-root artifacts/real_stream_validation/elec2 --max-samples 256
python -m autorl benchmark-suite --artifacts-root artifacts/real_stream_validation/suite --datasets elec2 --max-samples 256
python -m autorl phase10-suite --artifacts-root artifacts/phase10_experimental_series --series E1 --benchmark-datasets elec2 --benchmark-max-samples 128
```

Expected result:
- command exits successfully
- expected artifact paths are printed or persisted

## API Smoke Matrix

Start backend:

```bash
uvicorn autorl.interfaces.api.app:create_app --factory --reload
```

Verify:
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

Primary automated evidence:
- `tests/test_api_fastapi.py`

## UI Smoke Matrix

Start UI:

```bash
streamlit run src/autorl/interfaces/ui/app.py
```

Verify:
- forecast workflow opens
- built-in dataset analysis starts
- monitor section updates
- completed analysis is visible in reports/evidence
- export controls are available

Primary automated evidence:
- `tests/test_ui_streamlit.py`

## Artifact Verification

Must verify persisted artifacts exist for orchestrated experiments:
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

Benchmark replay artifacts:
- `summary.json`
- `summary.md`
- `decisions.csv`

Phase 10 benchmark support artifacts:
- `metrics.csv`
- `score_profile.png`

## Performance and Memory Checks

Required evidence:
- latency smoke for decision path
- memory smoke under pytest

Primary automated evidence:
- `tests/test_evaluator_metacontroller.py`
- `tests/test_state_and_exports.py`

## Documentation Completeness Check

Required files:
- `README.md`
- `docs/operations_manual.md`
- `docs/requirements_traceability.md`
- `docs/test_protocol.md`
- `docs/doc_01_use_case_diagram.md`
- `docs/doc_02_dfd_level_0.md`
- `docs/doc_03_component_diagram.md`
- `docs/doc_04_sequence_stay_switch.md`
- `docs/doc_05_state_machine.md`
- `docs/doc_06_er_schema.md`
- `docs/doc_07_deployment_diagram.md`
- `docs/doc_08_requirements_traceability.md`
- `docs/doc_09_moscow_requirements.md`
- `docs/doc_10_operational_instruction.md`

Primary automated evidence:
- `tests/test_phase11_docs.py`

## Final Acceptance Rule

Phase 11 is considered complete when:
- the required documentation artifacts exist;
- the traceability matrix covers all required requirement groups;
- the test protocol exists and references the final verification flow;
- import smoke passes;
- targeted Phase 11 documentation tests pass;
- regression tests pass, either as one run or as documented batches.
