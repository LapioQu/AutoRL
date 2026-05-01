# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-30T14:19:11.754561+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `hard_switch_lcb`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1265`
- feature_count: `4`
- next_prediction: `103.96383914203936`
- prediction_confidence: `0.9762` (high)

## Comparative Metrics

- adaptive_score: `0.949776`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937458`
- delta_vs_best_fixed: `+0.012318`
- oracle_score: `0.973752`
- oracle_gain: `0.036294`
- oracle_capture_ratio: `33.94%`
- final_strategy: `lin_lr_0_01`
- switch_count: `1`

## Interpretation

- Adaptive policy `hard_switch_lcb` finished on strategy `lin_lr_0_01` after 1 switches.
- It achieved `0.9498` against the best fixed baseline `knn_regressor` at `0.9375`.
- Oracle upper bound on this stream is `0.9738`. Available oracle gain over best fixed is `0.0363`, and the current adaptive controller captures `33.9%` of it.
- The uploaded stream looks non-stationary enough for adaptation to help: the gain over best fixed is `0.0123`.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `103.9638` based on the latest lagged context `['104.3', '104.23', '104.1']`.

## Caveats

- The stream is replayed in the original CSV row order.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Privacy Note

- Persisted reports intentionally exclude raw preview rows and full forecast-row payloads.
- Raw uploaded trajectories are not copied into the human-readable report layer.

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis`
- input_manifest_path: `artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\input_manifest.json`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141907-e75ac65f\analysis\summary.md`
