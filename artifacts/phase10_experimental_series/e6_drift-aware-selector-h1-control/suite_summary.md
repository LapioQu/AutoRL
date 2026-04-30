# Profile Suite Summary - e6_drift-aware-selector-h1-control

- profile_count: `1`
- dataset_count: `3`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.046875`
- delta_std: `0.025615`
- delta_ci95: `0.028986`
- effect_size_d: `-1.829983`
- paired_sign_test_p_value: `0.250000`
- wins_vs_best_fixed: `0`
- non_losses_vs_best_fixed: `0`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Airlines | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.761719 | 0.785156 | -0.023438 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\airlines\summary.json` |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.832031 | 0.906250 | -0.074219 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\summary.json` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 256 | 0.777344 | 0.820312 | -0.042969 | 0 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\summary.json` |
