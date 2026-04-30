# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:55:53.109457+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `recent_leader_meta`
- source_row_count: `512`
- source_rows_used: `512`
- sample_count: `509`
- feature_count: `3`
- next_prediction: `101.79`
- prediction_confidence: `0.9987` (high)

## Comparative Metrics

- adaptive_score: `0.940069`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.940069`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.964464`
- oracle_gain: `0.024396`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.9401` against the best fixed baseline `knn_regressor` at `0.9401`.
- Oracle upper bound on this stream is `0.9645`. Available oracle gain over best fixed is `0.0244`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `101.7900` based on the latest lagged context `['101.68', '102.15', '102.08']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-04-10 20:00:00+02:00",
  "water_flow_lps": "102.08"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 497 | 102.84 | 102.176 | {"target_lag_1": 102.23, "target_lag_2": 101.74, "target_lag_3": 101.14} |
| 498 | 103.04 | 102.304 | {"target_lag_1": 102.84, "target_lag_2": 102.23, "target_lag_3": 101.74} |
| 499 | 103.09 | 102.564 | {"target_lag_1": 103.04, "target_lag_2": 102.84, "target_lag_3": 102.23} |
| 500 | 102.84 | 102.434 | {"target_lag_1": 103.09, "target_lag_2": 103.04, "target_lag_3": 102.84} |
| 501 | 102.72 | 102.012 | {"target_lag_1": 102.84, "target_lag_2": 103.09, "target_lag_3": 103.04} |
| 502 | 102.67 | 101.85 | {"target_lag_1": 102.72, "target_lag_2": 102.84, "target_lag_3": 103.09} |
| 503 | 102.66 | 101.65599999999999 | {"target_lag_1": 102.67, "target_lag_2": 102.72, "target_lag_3": 102.84} |
| 504 | 102.38 | 100.934 | {"target_lag_1": 102.66, "target_lag_2": 102.67, "target_lag_3": 102.72} |
| 505 | 102.17 | 101.066 | {"target_lag_1": 102.38, "target_lag_2": 102.66, "target_lag_3": 102.67} |
| 506 | 101.68 | 101.036 | {"target_lag_1": 102.17, "target_lag_2": 102.38, "target_lag_3": 102.66} |
| 507 | 102.15 | 101.008 | {"target_lag_1": 101.68, "target_lag_2": 102.17, "target_lag_3": 102.38} |
| 508 | 102.08 | 101.71 | {"target_lag_1": 102.15, "target_lag_2": 101.68, "target_lag_3": 102.17} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\waterflow-20260429145551\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\waterflow-20260429145551\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\waterflow-20260429145551\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\waterflow-20260429145551`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429145551\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429145551\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429145551\auto_meta_selection\recent_leader_meta\summary.md`
