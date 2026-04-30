# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T13:28:00.551774+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `recent_leader_meta`
- source_row_count: `128`
- source_rows_used: `128`
- sample_count: `128`
- feature_count: `0`
- next_prediction: `90.00312883435582`
- prediction_confidence: `0.9003` (high)

## Comparative Metrics

- adaptive_score: `0.820469`
- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.820469`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.827149`
- oracle_gain: `0.006680`
- oracle_capture_ratio: `0.00%`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `tree_regressor` after 0 switches.
- It achieved `0.8205` against the best fixed baseline `tree_regressor` at `0.8205`.
- Oracle upper bound on this stream is `0.8271`. Available oracle gain over best fixed is `0.0067`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `90.0031` based on the latest lagged context `['102.9', '102.97', '103.12']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-03-25 18:00:00+01:00",
  "water_flow_lps": "103.12"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 116 | 104.23 | 70.86023355232044 | {} |
| 117 | 104.6 | 71.52762888127403 | {} |
| 118 | 105.17 | 72.18907630364855 | {} |
| 119 | 104.03 | 72.84869477757557 | {} |
| 120 | 103.93 | 74.09594698647255 | {} |
| 121 | 103.87 | 74.69262804674311 | {} |
| 122 | 104.02 | 75.27617548580825 | {} |
| 123 | 103.45 | 75.8510519760921 | {} |
| 124 | 102.81 | 89.6774213836478 | {} |
| 125 | 102.9 | 89.7595 | {} |
| 126 | 102.97 | 89.84111801242236 | {} |
| 127 | 103.12 | 89.92216049382715 | {} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\waterflow-20260429132800\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\waterflow-20260429132800\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\waterflow-20260429132800\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\waterflow-20260429132800`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132800\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132800\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132800\auto_meta_selection\recent_leader_meta\summary.md`
