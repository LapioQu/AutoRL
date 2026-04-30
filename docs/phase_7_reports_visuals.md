# Phase 7: reports and plots

Phase 7 adds reproducible experiment reporting artifacts on top of the phase 6 end-to-end execution path.

## Implemented scope

- markdown report generation as `report.md`
- reward curve export as `reward_curve.png`
- strategy timeline export as `strategy_timeline.png`
- utility/LCB export as `utility_lcb.png`
- summary tables and Stay/Switch breakdown inside the report
- reuse of persisted `metrics.csv`, `window_metrics.csv`, and `decisions.csv`

## Design notes

- reports are generated from real persisted experiment data, not hardcoded placeholders;
- PNG plots are produced by a small dependency-free renderer to keep the local stack minimal;
- report content includes configuration snapshot, seed, config hash, result summary, and Stay/Switch summary;
- the CLI `report` command now returns the generated markdown report.

## Verification

- integration tests assert report and plot files are created;
- tests verify PNG signatures for all exported plots;
- tests verify that the report contains config snapshot, seed, config hash, results summary, and Stay/Switch section.
