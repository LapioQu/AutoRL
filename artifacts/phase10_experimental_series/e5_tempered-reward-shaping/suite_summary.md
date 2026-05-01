# Profile Suite Summary - e5_tempered-reward-shaping

- profile_count: `2`
- dataset_count: `3`
- n: `3`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `-0.006355`
- delta_std: `0.010455`
- delta_ci95: `0.011831`
- oracle_gain_mean: `0.097982`
- oracle_gain_ci95: `0.055056`
- oracle_capture_mean: `0.019250`
- oracle_capture_ci95: `0.037731`
- effect_size_d: `-0.607818`
- paired_sign_test_p_value: `1.000000`
- wins_vs_best_fixed: `1`
- non_losses_vs_best_fixed: `1`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Oracle | Delta | Capture | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 45312 | 0.859441 | 0.876832 | 0.959393 | -0.017391 | 0.000000 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\elec2\summary.json` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 79986 | 0.767434 | 0.772510 | 0.924987 | -0.005076 | 0.000000 | 37 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift\insects_recurring\summary.json` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.897982 | 0.003402 | 0.057751 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e5_tempered-reward-shaping\h2_tempered_drift_regression\waterflow\summary.json` |
