# E9 - Baseline comparison

- mode: benchmark profile suite
- profiles: `hard_switch_lcb_regression`
- datasets: `WaterFlow`
- n: `1`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `1268`
- delta_mean: `-0.065067`
- delta_std: `0.000000`
- delta_ci95: `0.000000`
- effect_size_d: `-`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `0`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `1`
- profile_count: `1`
- sample_count_min: `1268`
- sample_count_max: `1268`
- consistent_sample_count: `True`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_switch_lcb | 1 | -0.065067 | 0.000000 | 0.000000 | 0 | 1.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.789125 | 0.854192 | -0.065067 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| WaterFlow | hard_switch_lcb_regression | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |
