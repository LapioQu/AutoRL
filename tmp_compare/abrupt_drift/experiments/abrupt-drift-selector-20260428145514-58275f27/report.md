# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | abrupt-drift-selector-20260428145514-58275f27 |
| Experiment Name | abrupt-drift-selector |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 52 |
| Config Hash | 7d59f7274ac5ca665dac4add3f165c6dfc58b29ca0324a1496673468ac36491c |
| Artifacts Path | `tmp_compare\abrupt_drift\experiments\abrupt-drift-selector-20260428145514-58275f27` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 53 |
| Switches | 1 |
| Fallback Decisions | 15 |
| Average Reward | 0.918816 |
| Success Rate | 0.816667 |
| Cumulative Reward | 55.128955 |
| Mean Window Variance | 0.015264 |
| Final Strategy | drift_aware |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | greedy_reward | drift_aware | - | 0.020000 | insufficient_samples |
| 1 | stay | greedy_reward | drift_aware | - | 0.020000 | insufficient_samples |
| 2 | stay | greedy_reward | drift_aware | - | 0.020000 | insufficient_samples |
| 3 | stay | greedy_reward | drift_aware | - | 0.020000 | insufficient_samples |
| 4 | stay | greedy_reward | drift_aware | -0.019482 | 0.020000 | no_candidate_improvement |
| 5 | stay | greedy_reward | drift_aware | -0.020883 | 0.020000 | no_candidate_improvement |
| 6 | stay | greedy_reward | drift_aware | -0.020988 | 0.020000 | no_candidate_improvement |
| 7 | stay | greedy_reward | drift_aware | -0.020999 | 0.020000 | no_candidate_improvement |
| 8 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 9 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 10 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 11 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 12 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 13 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 14 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 15 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 16 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 17 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 18 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |
| 19 | stay | greedy_reward | drift_aware | -0.021000 | 0.020000 | no_candidate_improvement |

_Showing first 20 of 53 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: abrupt-drift-selector
seed: 52
mode: adaptive
scenario:
  name: abrupt_drift
  episodes: 60
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: 30
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
  window_size: 8
  min_samples: 5
  delta: 0.01
  lambda: 0.3
  switch_cost: 0.01
  utility_weights:
    reward_mean: 1.0
    reward_variance: 0.25
    compute_cost: 0.15
    switch_cost: 0.6
artifacts_root: tmp_compare\abrupt_drift
tags:
- phase1
- abrupt_drift
notes: null
```
