# Phase 9 Streamlit UI

Phase 9 adds a local Streamlit interface over the same application services already used by the CLI and FastAPI layers.
This document is phase-scoped; final closure status across later work is tracked in [requirements_inventory.md](/E:/dipproj/docs/requirements_inventory.md).

## Implemented Scope

- one shared Streamlit app in `src/autorl/interfaces/ui/app.py`
- product-style visual shell with hero cards, styled metrics, and operator sidebar controls
- page-based information architecture with:
  - `Forecast Studio`
  - `Operations Monitor`
  - `Evidence`
- operations monitor page with `start`, `stop`, `rerun`, auto-refresh progress tracking, reward trace, and event log
- evidence page backed by `report.md`, compare rows, `versions.json`, and the artifact index
- dataset lab page for CSV upload or pasted CSV replay with:
  - one-page forecasting workflow
  - built-in dataset picker for `WaterFlow`, `Bikes`, `Elec2`, and `TrumpApproval`
  - target and order column selection
  - validation method selection for classification vs forecasting/regression
  - adaptive policy selection
  - manual row interpreter for schema-aware row append
  - support for one trailing blank-target row so the UI can predict that row directly
  - lag-based next-step prediction
  - adaptive vs best-fixed comparison
  - oracle upper bound and oracle capture reporting
  - local interpretation panel
  - human-readable validation errors instead of raw tracebacks
  - persisted dataset-lab artifacts
  - full-row default replay scope instead of short preview defaults
  - persisted dataset-lab history with detailed markdown reports

## Architectural Notes

- UI depends only on `ExperimentApiService`; it does not import repository, environment, evaluator, or domain switching logic directly.
- uploaded dataset analysis is handled by `DatasetLabService`, keeping replay and prediction logic out of the Streamlit layer.
- built-in datasets, manual-row normalization, and blank-target forecasting are also handled in `DatasetLabService`, so the Streamlit layer only orchestrates user flow and rendering.
- The app reads persisted SQLite rows and artifact files from the configured `artifacts_root`.
- `st.cache_resource` keeps one shared service instance per artifacts root so background runs survive Streamlit reruns.

## Verification

- `tests/test_ui_streamlit.py` drives a real UI workflow with `streamlit.testing.v1.AppTest`
- `tests/test_dataset_lab.py` verifies uploaded CSV replay, artifact persistence, and next-step prediction output
- `tests/test_dataset_lab.py` verifies persisted dataset-lab history and detailed report generation
- `tests/test_dataset_lab.py` also verifies manual-row interpretation and forecasting for an appended blank-target row
- the test creates persisted runs through shared services, starts one pending run from the UI, waits for terminal status, and verifies:
  - real metrics are shown
  - real decision rows are shown
  - real `report.md` content is shown
  - compare view reads two persisted experiments
  - export view lists real artifact paths
  - dataset lab accepts pasted CSV, interprets an appended manual row, and returns a next prediction for that row
  - dataset lab shows oracle-capture metrics for uploaded data

## Known Limits

- monitoring is refresh-based, not push-based
- export is exposed as artifact index plus local file-backed report/artifact views; ZIP/HTML export is still outside the current phase scope
