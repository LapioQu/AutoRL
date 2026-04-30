# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T13:27:15.453517+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `recent_leader_meta`
- source_row_count: `256`
- source_rows_used: `256`
- sample_count: `256`
- feature_count: `0`
- next_prediction: `95.51475644699144`
- prediction_confidence: `0.9839` (high)

## Comparative Metrics

- adaptive_score: `0.766907`
- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.766907`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.769485`
- oracle_gain: `0.002578`
- oracle_capture_ratio: `0.00%`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `tree_regressor` after 0 switches.
- It achieved `0.7669` against the best fixed baseline `tree_regressor` at `0.7669`.
- Oracle upper bound on this stream is `0.7695`. Available oracle gain over best fixed is `0.0026`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `95.5148` based on the latest lagged context `['100.85', '100.82', '100.38']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-03-31 04:00:00+02:00",
  "water_flow_lps": "100.38"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 244 | 101.84 | 95.24787425149704 | {} |
| 245 | 102.08 | 95.267552238806 | {} |
| 246 | 101.95 | 95.30798219584572 | {} |
| 247 | 101.68 | 95.36658823529415 | {} |
| 248 | 101.64 | 95.38510263929622 | {} |
| 249 | 101.51 | 95.40339181286554 | {} |
| 250 | 101.29 | 95.421195335277 | {} |
| 251 | 101.0 | 95.43825581395353 | {} |
| 252 | 100.84 | 95.45437681159424 | {} |
| 253 | 100.85 | 95.46994219653183 | {} |
| 254 | 100.82 | 95.485446685879 | {} |
| 255 | 100.38 | 95.500775862069 | {} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab\waterflow-20260429132715\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab\waterflow-20260429132715\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab\waterflow-20260429132715\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab\waterflow-20260429132715`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132715\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132715\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab\waterflow-20260429132715\auto_meta_selection\recent_leader_meta\summary.md`
