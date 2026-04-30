# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | baseline-adaptive-meta-final-20260428145802-3080a0ad |
| Experiment Name | baseline-adaptive_meta_final |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 52 |
| Config Hash | a6f1d9b47fd8378a506e42e4b9a89ab463f939a35a0dfa54ad9269311d7fa340 |
| Artifacts Path | `tmp_profiles\gradual2\adaptive_meta_final\experiments\baseline-adaptive-meta-final-20260428145802-3080a0ad` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 90 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.989667 |
| Success Rate | 1.000000 |
| Cumulative Reward | 89.069993 |
| Mean Window Variance | 0.000594 |
| Final Strategy | adaptive_meta_final |

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
experiment_name: baseline-adaptive_meta_final
seed: 52
mode: baseline
scenario:
  name: gradual_drift
  episodes: 90
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: 25
  drift_end_episode: 65
  fallback_patience: null
  tags: []
  description: null
strategies:
- name: adaptive_meta_final
  parameters:
    reward_weight: 0.2
    success_weight: 0.2
    fit_weight: 0.45
    recency_weight: 0.2
    cost_weight: 0.08
  enabled: true
  compute_cost: 0.12
  description: null
- name: fixed_low
  parameters:
    fixed_action_index: 0
  enabled: true
  compute_cost: 0.03
  description: null
- name: fixed_mid
  parameters:
    fixed_action_index: 1
  enabled: true
  compute_cost: 0.05
  description: null
- name: fixed_high
  parameters:
    fixed_action_index: 3
  enabled: true
  compute_cost: 0.07
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
artifacts_root: tmp_profiles/gradual2/adaptive_meta_final
tags: []
notes: null
```
