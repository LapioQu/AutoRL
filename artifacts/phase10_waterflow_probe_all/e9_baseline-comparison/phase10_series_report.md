# E9 - Baseline comparison

- mode: benchmark profile suite
- profiles: `adaptive_meta_final_regression, greedy_reward_regression, h1_drift_aware_v2_regression, h2_tempered_drift_regression, hard_switch_lcb_regression`
- datasets: `WaterFlow`
- n: `5`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `1268`
- delta_mean: `-0.048673`
- delta_std: `0.019138`
- delta_ci95: `0.016775`
- effect_size_d: `-2.543317`
- paired_sign_test_p_value: `0.062500`
- wins_vs_best_fixed: `0`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `1`
- profile_count: `5`
- sample_count_min: `1268`
- sample_count_max: `1268`
- consistent_sample_count: `True`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_share_portfolio | 1 | -0.020135 | 0.000000 | 0.000000 | 0 | 6.000000 |
| hard_switch_lcb | 3 | -0.061299 | 0.006527 | 0.007385 | 0 | 1.000000 |
| recent_leader_meta | 1 | -0.039335 | 0.000000 | 0.000000 | 0 | 2.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| WaterFlow | adaptive_meta_final_regression | fixed_share_portfolio | normalized_reward | 1268 | 0.834057 | 0.854192 | -0.020135 | 6 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.md` |
| WaterFlow | greedy_reward_regression | recent_leader_meta | normalized_reward | 1268 | 0.814857 | 0.854192 | -0.039335 | 2 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.789125 | 0.854192 | -0.065067 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.md` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.824297 | 0.878059 | -0.053762 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.md` |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.789125 | 0.854192 | -0.065067 | 1 | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| WaterFlow | adaptive_meta_final_regression | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.md` |
| WaterFlow | greedy_reward_regression | `E:\dipproj\configs\benchmark_profiles\greedy_reward_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.md` |
| WaterFlow | h2_tempered_drift_regression | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.md` |
| WaterFlow | hard_switch_lcb_regression | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb_regression.yaml` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_waterflow_probe_all\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |
