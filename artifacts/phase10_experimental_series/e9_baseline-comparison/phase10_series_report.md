# E9 - Baseline comparison

- mode: benchmark profile suite
- profiles: `adaptive_meta_final, greedy_reward, h1_drift_aware_v2, h2_tempered_drift, hard_switch_lcb`
- datasets: `Airlines, Elec2, InsectsRecurring`
- n: `15`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- max_samples: `256`
- delta_mean: `-0.045573`
- delta_std: `0.020652`
- delta_ci95: `0.010452`
- effect_size_d: `-2.206670`
- paired_sign_test_p_value: `0.000061`
- wins_vs_best_fixed: `0`
- suite_summary_json_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\suite_summary.json`
- suite_summary_md_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\suite_summary.md`
- primary_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_delta_vs_best_fixed.png`
- switches_plot_path: `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\phase10_switch_count.png`

## Benchmark Protocol

- dataset_count: `3`
- profile_count: `5`
- sample_count_min: `256`
- sample_count_max: `256`
- consistent_sample_count: `True`
- interpretation_note: `Benchmark replay rows are deterministic temporal streams; inferential statistics are computed over dataset/profile result deltas and should be read as cautious phase-level evidence, not as a claim of universal superiority.`

## Policy Aggregates

| Policy | n | Delta Mean | Delta Std | Delta CI95 | Wins vs Best Fixed | Mean Switch Count |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hard_switch_lcb | 12 | -0.046875 | 0.021845 | 0.012360 | 0 | 0.000000 |
| recent_leader_meta | 3 | -0.040365 | 0.017614 | 0.019932 | 0 | 1.333333 |

## Benchmark Results

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Report |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Airlines | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\summary.md` |
| Elec2 | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.md` |
| InsectsRecurring | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.md` |
| Airlines | greedy_reward | recent_leader_meta | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\summary.md` |
| Elec2 | greedy_reward | recent_leader_meta | accuracy | 256 | 0.867188 | 0.906250 | -0.039062 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.md` |
| InsectsRecurring | greedy_reward | recent_leader_meta | accuracy | 256 | 0.761719 | 0.820312 | -0.058594 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.md` |
| Airlines | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\summary.md` |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.md` |
| Airlines | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\summary.md` |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.md` |
| Airlines | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\summary.md` |
| Elec2 | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.md` |
| InsectsRecurring | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.md` |

## Artifact Coverage

| Dataset | Profile | Config | Metrics | Decisions | Plot | Report |
| --- | --- | --- | --- | --- | --- | --- |
| Airlines | adaptive_meta_final | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\summary.md` |
| Elec2 | adaptive_meta_final | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.md` |
| InsectsRecurring | adaptive_meta_final | `E:\dipproj\configs\benchmark_profiles\adaptive_meta_final.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.md` |
| Airlines | greedy_reward | `E:\dipproj\configs\benchmark_profiles\greedy_reward.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\summary.md` |
| Elec2 | greedy_reward | `E:\dipproj\configs\benchmark_profiles\greedy_reward.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.md` |
| InsectsRecurring | greedy_reward | `E:\dipproj\configs\benchmark_profiles\greedy_reward.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.md` |
| Airlines | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\summary.md` |
| Elec2 | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.md` |
| InsectsRecurring | h1_drift_aware_v2 | `E:\dipproj\configs\benchmark_profiles\h1_drift_aware_v2.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.md` |
| Airlines | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\summary.md` |
| Elec2 | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.md` |
| InsectsRecurring | h2_tempered_drift | `E:\dipproj\configs\benchmark_profiles\h2_tempered_drift.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.md` |
| Airlines | hard_switch_lcb | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\summary.md` |
| Elec2 | hard_switch_lcb | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.md` |
| InsectsRecurring | hard_switch_lcb | `E:\dipproj\configs\benchmark_profiles\hard_switch_lcb.yaml` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\metrics.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\decisions.csv` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\score_profile.png` | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.md` |
