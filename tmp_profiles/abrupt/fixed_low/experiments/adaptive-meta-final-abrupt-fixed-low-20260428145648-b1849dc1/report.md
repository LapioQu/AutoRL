# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | adaptive-meta-final-abrupt-fixed-low-20260428145648-b1849dc1 |
| Experiment Name | adaptive-meta-final-abrupt-fixed_low |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 42 |
| Config Hash | 92e124e3c494490e6cfa9d566554f7303cb2fdf34eb858935677967109cc53ab |
| Artifacts Path | `tmp_profiles\abrupt\fixed_low\experiments\adaptive-meta-final-abrupt-fixed-low-20260428145648-b1849dc1` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 80 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.940878 |
| Success Rate | 1.000000 |
| Cumulative Reward | 75.270278 |
| Mean Window Variance | 0.000065 |
| Final Strategy | fixed_low |

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
experiment_name: adaptive-meta-final-abrupt-fixed_low
seed: 42
mode: baseline
scenario:
  name: abrupt_drift
  episodes: 80
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: 40
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags: []
  description: null
strategies:
- name: fixed_low
  parameters:
    fixed_action_index: 0
  enabled: true
  compute_cost: 0.03
  description: null
meta_controller:
  window_size: 8
  min_samples: 5
  delta: 0.01
  lambda: 0.3
  switch_cost: 0.01
  utility_weights:
    reward_mean: 1.0
    reward_variance: 0.15
    compute_cost: 0.08
    switch_cost: 0.2
artifacts_root: tmp_profiles/abrupt/fixed_low
tags: []
notes: null
```
