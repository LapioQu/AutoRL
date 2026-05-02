# Phase 10 Experimental Series

Phase 10 is persisted by `Phase10ExperimentalSeriesRunner` in:

- `artifacts/phase10_experimental_series/phase10_suite_summary.json`
- `artifacts/phase10_experimental_series/phase10_suite_report.md`

Each series stores:
- `phase10_series_summary.json`
- `phase10_series_report.md`
- primary plot
- `phase10_switch_count.png`
- nested experiment or replay artifacts

## Realized Series

| Series | Title | Type | Current Scope |
| --- | --- | --- | --- |
| `E1` | Stationary control | seeded experiment suite | full configured controlled scenario |
| `E2` | Abrupt drift | seeded experiment suite | full configured controlled scenario |
| `E3` | Gradual drift | seeded experiment suite | full configured controlled scenario |
| `E4` | Noisy reward | seeded experiment suite | full configured controlled scenario |
| `E5` | Tempered reward shaping | benchmark profile suite | full `Elec2`, full `InsectsRecurring`, full `WaterFlow` |
| `E6` | Drift-aware selector / H1 control | benchmark profile suite | full `Elec2`, full `InsectsRecurring`, full `WaterFlow` |
| `E7` | Reproducibility | seeded experiment suite | repeated controlled scenario |
| `E8` | Fallback insufficient data | seeded experiment suite | full configured controlled scenario |
| `E9` | Baseline comparison | benchmark profile suite | full `Elec2`, full `InsectsRecurring`, full `WaterFlow` |

## Benchmark Protocol

Current benchmark protocol for `E5`, `E6`, and `E9`:

- full datasets, no `max_samples` truncation
- deterministic temporal replay
- benchmark datasets:
  - `Elec2` (`45312` samples)
  - `InsectsRecurring` (`79986` samples)
  - `WaterFlow` (`1268` samples)

`Airlines` full replay was excluded from the current final Phase 10 benchmark set because its full length (`539383` samples) is disproportionately larger and makes the benchmark suite operationally unbalanced relative to the other selected streams.

## Artifact Shape

### Seeded series

Each controlled-series run references:
- `config.yaml`
- `metrics.csv`
- `decisions.csv`
- `report.md`
- `report.html`
- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`
- `versions.json`

### Benchmark series

Each benchmark result references:
- `artifact_root_path`
- `config_path`
- `metrics_path`
- `decision_csv_path`
- `summary_json_path`
- `report_md_path`
- `plots_path`

Each benchmark series summary also contains:
- `n`
- `seed_protocol`
- `delta_mean`
- `delta_std`
- `delta_ci95`
- `oracle_gain_mean`
- `oracle_capture_mean`
- `effect_size_d`
- `paired_sign_test_p_value`
- `benchmark_protocol`

## Current Experimental Outcome

The current full-dataset benchmark outcome is:

- `E5`: near-neutral overall, with positive `WaterFlow` and negative `Elec2` / `InsectsRecurring`
- `E6`: still negative overall, but `WaterFlow` is positive under the system LCB path
- `E9`: still slightly negative on average against `best fixed`, but now exposes the full `oracle_gain / oracle_capture_ratio` picture across `Elec2`, `InsectsRecurring`, and `WaterFlow`

This means Phase 10 currently serves as:
- behavioral validation of the system
- full-stream benchmark evidence

It now provides **mixed superiority evidence**:

- positive forecasting evidence on `WaterFlow`
- weak-to-negative classification evidence on `Elec2` and `InsectsRecurring`
- explicit oracle-capacity evidence showing that the negative classification rows are not caused by zero adaptive headroom

### WaterFlow Interpretation

`WaterFlow` was added because it is the forecasting/regression stream in the current phase-10 benchmark set.

What the resulting artifacts show:

- switching does happen on `WaterFlow`
- oracle gain does exist on the `WaterFlow` forecasting stream
- and the system forecasting path can outperform `best fixed`

For the system forecasting path now used in phase-10 WaterFlow rows:

- `hard_switch_lcb_regression`: `+0.002097`
- `h2_tempered_drift_regression`: `+0.003402`
- `adaptive_meta_final_regression`: `+0.032334`
- `adaptive_meta_final_regression` oracle capture: `46.15%`
- `hard_switch_lcb_regression` oracle capture: `2.99%`
- `h2_tempered_drift_regression` oracle capture: `5.78%`

So the earlier poor WaterFlow result was **not** because `WaterFlow` is stationary and **not** because oracle gain is zero.
It happened because the generic benchmark path was using a broader raw regression registry with a stronger `windowed_rf` best-fixed baseline.

After switching WaterFlow to the same tuned forecasting path as the system benchmark:

- best fixed reverted to the tuned stationary portfolio baseline (`lin_lr_0_001`)
- the system LCB became positive again
- the adaptive-meta profile again selected `fixed_share_portfolio` and recovered the strongest WaterFlow result

### Oracle-Based Interpretation

Phase 10 benchmark summaries now expose:

- `oracle_score`
- `oracle_gain`
- `oracle_capture_ratio`

This makes the benchmark rows interpretable without guessing whether a weak `delta vs best fixed` came from:

- no real adaptive opportunity in the stream, or
- a controller that failed to capture available adaptive upside.

In the current full-dataset Phase 10 benchmark bundle:

- `WaterFlow` has real adaptive headroom and positive capture in the system forecasting path
- `Elec2` and `InsectsRecurring` still show substantial oracle gain, but the current generic classification benchmark controllers capture little or none of it

So the Phase 10 benchmark story is now explicit:

- forecasting on `WaterFlow` validates that the system can exploit non-stationarity under the tuned system path
- classification benchmark rows remain the weaker part of the current Phase 10 evidence package
