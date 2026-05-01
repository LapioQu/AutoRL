# Profile Suite Summary - e9_baseline-comparison

- profile_count: `10`
- dataset_count: `3`
- n: `15`
- seed_protocol: `deterministic_temporal_replay_no_rng`
- seeds: `[]`
- delta_mean: `0.000357`
- delta_std: `0.009271`
- delta_ci95: `0.004692`
- effect_size_d: `0.038533`
- paired_sign_test_p_value: `0.118469`
- wins_vs_best_fixed: `4`
- non_losses_vs_best_fixed: `4`

| Dataset | Profile | Policy | Score | Samples | Adaptive | Best Fixed | Delta | Switches | Summary |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Elec2 | adaptive_meta_final | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\elec2\summary.json` |
| InsectsRecurring | adaptive_meta_final | fixed_share_portfolio | accuracy | 79986 | 0.769585 | 0.772510 | -0.002926 | 367 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final\insects_recurring\summary.json` |
| WaterFlow | adaptive_meta_final_regression | fixed_share_portfolio | normalized_reward | 1268 | 0.836279 | 0.803945 | 0.032334 | 10 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\adaptive_meta_final_regression\waterflow\summary.json` |
| Elec2 | greedy_reward | recent_leader_meta | accuracy | 45312 | 0.876523 | 0.876832 | -0.000309 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\elec2\summary.json` |
| InsectsRecurring | greedy_reward | recent_leader_meta | accuracy | 79986 | 0.771372 | 0.772510 | -0.001138 | 11 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward\insects_recurring\summary.json` |
| WaterFlow | greedy_reward_regression | recent_leader_meta | normalized_reward | 1268 | 0.803759 | 0.803945 | -0.000186 | 1 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\greedy_reward_regression\waterflow\summary.json` |
| Elec2 | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\elec2\summary.json` |
| InsectsRecurring | h1_drift_aware_v2 | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2\insects_recurring\summary.json` |
| WaterFlow | h1_drift_aware_v2_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h1_drift_aware_v2_regression\waterflow\summary.json` |
| Elec2 | h2_tempered_drift | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\elec2\summary.json` |
| InsectsRecurring | h2_tempered_drift | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift\insects_recurring\summary.json` |
| WaterFlow | h2_tempered_drift_regression | hard_switch_lcb | normalized_reward | 1268 | 0.842475 | 0.839073 | 0.003402 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\h2_tempered_drift_regression\waterflow\summary.json` |
| Elec2 | hard_switch_lcb | hard_switch_lcb | accuracy | 45312 | 0.872263 | 0.876832 | -0.004568 | 2 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\elec2\summary.json` |
| InsectsRecurring | hard_switch_lcb | hard_switch_lcb | accuracy | 79986 | 0.768597 | 0.772510 | -0.003913 | 36 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb\insects_recurring\summary.json` |
| WaterFlow | hard_switch_lcb_regression | hard_switch_lcb | normalized_reward | 1268 | 0.806041 | 0.803945 | 0.002097 | 4 | `E:\dipproj\artifacts\phase10_experimental_series\e9_baseline-comparison\hard_switch_lcb_regression\waterflow\summary.json` |
