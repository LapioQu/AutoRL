# UI Acceptance Checklist

Phase 9 acceptance checklist against the T3 UI scope.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Create experiment without editing code | passed | `src/autorl/interfaces/ui/app.py`, `tests/test_ui_streamlit.py` |
| Start experiment and see status in UI | passed | `Run / Monitor` tab, `tests/test_ui_streamlit.py` |
| View reward and utility/LCB visuals | passed | `Metrics Dashboard` tab, generated `utility_lcb.png` |
| View active strategy timeline | passed | `Strategy Timeline` tab |
| View Stay/Switch journal with reasons | passed | `Decision Journal` tab |
| Compare baseline and adaptive runs | passed | `Compare Strategies` tab |
| View report and exportable artifact index | passed | `Reports / Export` tab |
| View reproducibility block | passed | overview and report tabs |
| UI reads real artifacts and data | passed | `tests/test_ui_streamlit.py` |
| No hardcoded fake results | passed | UI pulls all run data from `ExperimentApiService` and artifact files |
| Upload or paste dataset and get next prediction | passed | `Dataset Lab` tab, `tests/test_dataset_lab.py`, `tests/test_ui_streamlit.py` |
| Live progress updates without manual metric reload | passed in refresh-based mode | `Run / Monitor` auto-refresh and progress bar |
| Primary navigation reflects operational user workflow | passed | `Forecast Studio`, `Operations Monitor`, `Evidence` |
