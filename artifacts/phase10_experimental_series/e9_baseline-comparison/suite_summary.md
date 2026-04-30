# Profile Suite Summary - e9_baseline-comparison

- profile_count: `5`
- dataset_count: `3`
- n: `15`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.045573`
- delta_std: `0.020652`
- delta_ci95: `0.010452`
- effect_size_d: `-2.206670`
- paired_sign_test_p_value: `0.000061`
- wins_vs_best_fixed: `0`
- non_losses_vs_best_fixed: `0`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Airlines | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\airlines\summary.json` |
| Elec2 | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.json` |
| InsectsRecurring | adaptive_meta_final | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.json` |
| Airlines | greedy_reward | recent_leader_meta | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\airlines\summary.json` |
| Elec2 | greedy_reward | recent_leader_meta | accuracy | 256 | 0.867188 | 0.906250 | -0.039062 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.json` |
| InsectsRecurring | greedy_reward | recent_leader_meta | accuracy | 256 | 0.761719 | 0.820312 | -0.058594 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.json` |
| Airlines | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\airlines\summary.json` |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.json` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.json` |
| Airlines | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\airlines\summary.json` |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.json` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.json` |
| Airlines | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\airlines\summary.json` |
| Elec2 | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.json` |
| InsectsRecurring | hard_switch_lcb | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.json` |
