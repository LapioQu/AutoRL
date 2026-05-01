# Dataset Lab Report

## Summary

- created_at_utc: `2026-04-30T14:16:26.947822+00:00`
- dataset_name: `WaterFlow`
- task_type: `regression`
- target_column: `water_flow_lps`
- policy_name: `recent_leader_meta`
- source_row_count: `1268`
- source_rows_used: `1268`
- sample_count: `1265`
- feature_count: `3`
- next_prediction: `102.66799999999999`
- prediction_confidence: `0.9762` (high)

## Comparative Metrics

- adaptive_score: `0.937470`
- best_fixed_strategy: `knn_regressor`
- best_fixed_score: `0.937470`
- delta_vs_best_fixed: `+0.000000`
- oracle_score: `0.973752`
- oracle_gain: `0.036282`
- oracle_capture_ratio: `0.00%`
- final_strategy: `knn_regressor`
- switch_count: `0`

## Interpretation

- Adaptive policy `recent_leader_meta` finished on strategy `knn_regressor` after 0 switches.
- It achieved `0.9375` against the best fixed baseline `knn_regressor` at `0.9375`.
- Oracle upper bound on this stream is `0.9738`. Available oracle gain over best fixed is `0.0363`, and the current adaptive controller captures `0.0%` of it.
- Adaptive and best fixed finished effectively tied on this stream.
- No strategy changes were needed; the stream behaved close to one dominant regime.
- The forecast target is the next step after the last fully observed row in the stream.
- Next-step forecast from the final adaptive strategy is `102.6680` based on the latest lagged context `['104.3', '104.23', '104.1']`.

## Caveats

- The stream is replayed in the selected order column.
- Automatic lag generation uses the previous `3` observed target values.
- The quality score is a bounded normalized reward, not raw MAE or RMSE.
- If future exogenous features are unknown, the next prediction reuses the latest available covariate snapshot.

## Privacy Note

- Persisted reports intentionally exclude raw preview rows and full forecast-row payloads.
- Raw uploaded trajectories are not copied into the human-readable report layer.

## Visual Artifacts

- score_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\dataset_lab_scores.png`
- portfolio_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\dataset_lab_portfolio.png`
- switch_plot_path: `artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\dataset_lab_switches.png`

## Artifact Paths

- artifact_root: `artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis`
- input_manifest_path: `artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\input_manifest.json`
- replay_summary_json_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\auto_meta_selection\recent_leader_meta\summary.json`
- decision_csv_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\auto_meta_selection\recent_leader_meta\decisions.csv`
- replay_report_md_path: `E:\dipproj\artifacts\dataset_lab_jobs\waterflow-20260430141623-c20cb8fd\analysis\auto_meta_selection\recent_leader_meta\summary.md`
