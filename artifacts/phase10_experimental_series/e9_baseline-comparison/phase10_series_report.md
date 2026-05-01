# E9 - Baseline comparison

- mode: benchmark profile suite
- profiles: `adaptive_meta_final, adaptive_meta_final_regression, greedy_reward, greedy_reward_regression, h1_drift_aware_v2, h1_drift_aware_v2_regression, h2_tempered_drift, h2_tempered_drift_regression, hard_switch_lcb, hard_switch_lcb_regression`
- datasets: `Elec2, InsectsRecurring, WaterFlow`
- n: `15`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `None`
- delta_mean: `-0.002249`
- delta_std: `0.011917`
- delta_ci95: `0.006031`
- oracle_gain_mean: `0.100957`
- oracle_gain_ci95: `0.019388`
- oracle_capture_mean: `0.038606`
- oracle_capture_ci95: `0.059839`
- effect_size_d: `-0.188746`
- paired_sign_test_p_value: `0.118469`
- wins_vs_best_fixed: `4`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `3`
- profile_count: `10`
- sample_count_min: `1268`
- sample_count_max: `79986`
- consistent_sample_count: `False`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Oracle Gain Mean | Capture Mean | Capture CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed_share_portfolio | 2 | 0.014511 | 0.025207 | 0.034934 | 0.111271 | 0.230744 | 0.452258 | 1 | 184.000000 |
| hard_switch_lcb | 9 | -0.006645 | 0.008715 | 0.005694 | 0.100461 | 0.013067 | 0.013839 | 3 | 15.000000 |
| recent_leader_meta | 4 | -0.000739 | 0.000399 | 0.000391 | 0.096916 | 0.000000 | 0.000000 | 0 | 5.000000 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | adaptive_meta_final | recent_leader_meta | accuracy | 45312 | 0.876015 | 0.876832 | 0.959393 | -0.000817 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.md` |
| InsectsRecurring | adaptive_meta_final | fixed_share_portfolio | accuracy | 79986 | 0.769197 | 0.772510 | 0.924987 | -0.003313 | 0.000000 | 358 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.md` |
| WaterFlow | adaptive_meta_final_regression | fixed_share_portfolio | normalized_reward | 1268 | 0.836279 | 0.803945 | 0.874010 | 0.032334 | 0.461488 | 10 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.md` |
| Elec2 | greedy_reward | recent_leader_meta | accuracy | 45312 | 0.876015 | 0.876832 | 0.959393 | -0.000817 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.md` |
| InsectsRecurring | greedy_reward | recent_leader_meta | accuracy | 79986 | 0.771372 | 0.772510 | 0.924987 | -0.001138 | 0.000000 | 11 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.md` |
| WaterFlow | greedy_reward_regression | recent_leader_meta | normalized_reward | 1268 | 0.803759 | 0.803945 | 0.874010 | -0.000186 | 0.000000 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.md` |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 45312 | 0.859441 | 0.876832 | 0.959393 | -0.017391 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 79986 | 0.767434 | 0.772510 | 0.924987 | -0.005076 | 0.000000 | 37 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.874010 | 0.002097 | 0.029925 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.md` |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 45312 | 0.859441 | 0.876832 | 0.959393 | -0.017391 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 79986 | 0.767434 | 0.772510 | 0.924987 | -0.005076 | 0.000000 | 37 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.md` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.897982 | 0.003402 | 0.057751 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.md` |
| Elec2 | hard_switch_lcb | hard_switch_lcb | accuracy | 45312 | 0.859441 | 0.876832 | 0.959393 | -0.017391 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.md` |
| InsectsRecurring | hard_switch_lcb | hard_switch_lcb | accuracy | 79986 | 0.767434 | 0.772510 | 0.924987 | -0.005076 | 0.000000 | 37 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.md` |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.874010 | 0.002097 | 0.029925 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| Elec2 | adaptive_meta_final | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.md` |
| InsectsRecurring | adaptive_meta_final | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.md` |
| WaterFlow | adaptive_meta_final_regression | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.md` |
| Elec2 | greedy_reward | `E:\dipproj\configs\benchmark_profiles\greedy_reward.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.md` |
| InsectsRecurring | greedy_reward | `E:\dipproj\configs\benchmark_profiles\greedy_reward.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.md` |
| WaterFlow | greedy_reward_regression | `E:\dipproj\configs\benchmark_profiles\greedy_reward_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.md` |
| Elec2 | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.md` |
| WaterFlow | h1_drift_aware_v2_regression | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.md` |
| Elec2 | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.md` |
| WaterFlow | h2_tempered_drift_regression | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.md` |
| Elec2 | hard_switch_lcb | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.md` |
| InsectsRecurring | hard_switch_lcb | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.md` |
| WaterFlow | hard_switch_lcb_regression | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb_regression.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.md` |
