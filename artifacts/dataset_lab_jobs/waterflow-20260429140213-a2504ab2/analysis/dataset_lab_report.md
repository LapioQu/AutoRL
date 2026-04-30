# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-29T14:02:14.072630+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `hard_switch_lcb`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1268`
- feature_count: `0`
- next_prediction: `103.63754768130454`
- prediction_confidence: `0.9984` (high)

## Comparative Metrics

- adaptive_score: `0.863475`
- best_fixed_strategy: `tree_regressor`
- best_fixed_score: `0.863475`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.868042`
- oracle_gain: `0.004568`
- oracle_capture_ratio: `0.00%`
- final_strategy: `tree_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `hard_switch_lcb` finished on strategy `tree_regressor` after 0 switches.
- It achieved `0.8635` against the best fixed baseline `tree_regressor` at `0.8635`.
- Oracle upper bound on this stream is `0.8680`. Available oracle gain over best fixed is `0.0046`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `103.6375` based on the latest lagged context `['104.3', '104.23', '104.1']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Forecast Row

```json
{
  "Time": "2022-05-16 22:00:00+02:00",
  "water_flow_lps": "104.1"
}
```

## Recent Adaptive Preview

| row_index | actual_target | adaptive_prediction | feature_snapshot |
| --- | --- | --- | --- |
| 1256 | 104.39 | 103.26417244157686 | {} |
| 1257 | 104.71 | 103.33172209508226 | {} |
| 1258 | 104.77 | 103.35928765318062 | {} |
| 1259 | 104.69 | 103.387501900117 | {} |
| 1260 | 104.69 | 103.41355186211466 | {} |
| 1261 | 104.64 | 103.43908082487236 | {} |
| 1262 | 104.59 | 103.46309920837491 | {} |
| 1263 | 104.62 | 103.50817524003992 | {} |
| 1264 | 104.65 | 103.53041173523911 | {} |
| 1265 | 104.3 | 103.57519526582955 | {} |
| 1266 | 104.23 | 103.58969136051296 | {} |
| 1267 | 104.1 | 103.62810987888219 | {} |

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260429140213-a2504ab2\analysis\summary.md`
