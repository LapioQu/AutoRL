# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | abrupt-drift-selector-greedy-reward-baseline-20260428145518-64d85a27 |
| Experiment Name | abrupt-drift-selector-greedy_reward-baseline |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 52 |
| Config Hash | bf71ab286c45770045f3651cef19f3a549b7ebf35746ab73e33c7d361082d6f0 |
| Artifacts Path | `tmp_compare\abrupt_drift\greedy_reward\experiments\abrupt-drift-selector-greedy-reward-baseline-20260428145518-64d85a27` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.930369 |
| Success Rate | 1.000000 |
| Cumulative Reward | 55.822166 |
| Mean Window Variance | 0.000081 |
| Final Strategy | greedy_reward |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: abrupt-drift-selector-greedy_reward-baseline
seed: 52
mode: baseline
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
artifacts_root: tmp_compare\abrupt_drift\greedy_reward
tags:
- phase1
- abrupt_drift
notes: null
```
