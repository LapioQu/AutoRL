# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T12:37:39.480812+00:00`
- dataset_name: `uploaded-classification`
- task_type: `classification`
- target_column: `target`
- policy_name: `recent_leader_meta`
- source_row_count: `12`
- source_rows_used: `12`
- sample_count: `12`
- feature_count: `2`
- next_prediction: `high`
- prediction_confidence: `0.5714` (medium)

## Comparative Metrics

- adaptive_score: `0.750000`
- best_fixed_strategy: `softmax_lr_0_20`
- best_fixed_score: `0.750000`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.833333`
- oracle_gain: `0.083333`
- oracle_capture_ratio: `0.00%`
- final_strategy: `softmax_lr_0_20`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `softmax_lr_0_20` after 0 switches.
- It achieved `0.7500` against the best fixed baseline `softmax_lr_0_20` at `0.7500`.
- Oracle upper bound on this stream is `0.8333`. Available oracle gain over best fixed is `0.0833`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step class from the final adaptive strategy is `high` based on the latest lagged context `['low', 'low', 'mid']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is prequential accuracy over the uploaded stream.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "moment": "12",
  "signal_a": "0.60",
  "signal_b": "1.6",
  "target": "mid"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 0 | low | low | {"signal_a": 0.1, "signal_b": 1} |
| 1 | low | low | {"signal_a": 0.15, "signal_b": 1} |
| 2 | low | low | {"signal_a": 0.2, "signal_b": 1.1} |
| 3 | mid | low | {"signal_a": 0.4, "signal_b": 1.3} |
| 4 | mid | mid | {"signal_a": 0.45, "signal_b": 1.4} |
| 5 | mid | mid | {"signal_a": 0.55, "signal_b": 1.5} |
| 6 | high | mid | {"signal_a": 0.8, "signal_b": 1.8} |
| 7 | high | high | {"signal_a": 0.85, "signal_b": 1.9} |
| 8 | high | high | {"signal_a": 0.95, "signal_b": 2} |
| 9 | low | low | {"signal_a": 0.3, "signal_b": 1.2} |
| 10 | low | low | {"signal_a": 0.35, "signal_b": 1.2} |
| 11 | mid | high | {"signal_a": 0.6, "signal_b": 1.6} |

## Visual Artifacts

- score_plot_path: `artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739`
- replay_summary_json_path: `E:\dipproj\artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\ui_generic_fix_check_uploads2\dataset_lab\uploaded-classification-20260429123739\auto_meta_selection\recent_leader_meta\summary.md`
