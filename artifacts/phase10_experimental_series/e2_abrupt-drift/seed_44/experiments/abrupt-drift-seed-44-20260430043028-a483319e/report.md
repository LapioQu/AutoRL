# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | abrupt-drift-seed-44-20260430043028-a483319e |
| Experiment Name | abrupt_drift-seed-44 |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 44 |
| Config Hash | 9197a510605ebc8b7e86d5d45dda3947ce336ee1797a8f1f342143803240a2b7 |
| Artifacts Path | `E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\seed_44\experiments\abrupt-drift-seed-44-20260430043028-a483319e` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 150 |
| Decisions | 133 |
| Switches | 1 |
| Fallback Decisions | 11 |
| Average Reward | 0.973832 |
| Success Rate | 0.913333 |
| Cumulative Reward | 146.074857 |
| Mean Window Variance | 0.014942 |
| Final Strategy | drift_aware |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 1 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 2 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 3 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 4 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 5 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 6 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 7 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 8 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 9 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 10 | stay | greedy_reward | drift_aware | - | 0.260000 | insufficient_samples |
| 11 | stay | greedy_reward | drift_aware | -0.134730 | 0.260000 | no_candidate_improvement |
| 12 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 13 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 14 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 15 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 16 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 17 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 18 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |
| 19 | stay | greedy_reward | drift_aware | -0.135000 | 0.260000 | no_candidate_improvement |

_Showing first 20 of 133 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: abrupt_drift-seed-44
seed: 44
mode: adaptive
scenario:
  name: abrupt_drift
  episodes: 150
  steps_per_episode: 60
  reward_noise_std: 0.0
  drift_episode: 75
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - drift
  - abrupt
  description: Reward regime changes sharply at one episode boundary.
strategies:
- name: greedy_reward
  parameters:
    epsilon: 0.05
  enabled: true
  compute_cost: 0.08
  description: null
- name: drift_aware
  parameters:
    detector_window: 15
    trigger_zscore: 2.5
  enabled: true
  compute_cost: 0.18
  description: null
meta_controller:
  window_size: 18
  min_samples: 12
  delta: 0.06
  lambda: 1.2
  switch_cost: 0.2
  utility_weights:
    compute_cost: 0.15
    reward_mean: 1.0
    reward_variance: 0.25
    switch_cost: 0.6
artifacts_root: E:\dipproj\artifacts\phase10_experimental_series\e2_abrupt-drift\seed_44
tags:
- phase1
- abrupt_drift
notes: null
```
