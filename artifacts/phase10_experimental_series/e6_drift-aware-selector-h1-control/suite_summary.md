# Profile Suite Summary - e6_drift-aware-selector-h1-control

- profile_count: `2`
- dataset_count: `3`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.002128`
- delta_std: `0.003674`
- delta_ci95: `0.004157`
- effect_size_d: `-0.579347`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `1`
- non_losses_vs_best_fixed: `1`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\elec2\summary.json` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2\insects_recurring\summary.json` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e6_drift-aware-selector-h1-control\h1_drift_aware_v2_regression\waterflow\summary.json` |
