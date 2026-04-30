# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | gradual-drift-selector-adaptive-meta-baseline-20260428145532-7f6ea6d1 |
| Experiment Name | gradual-drift-selector-adaptive_meta-baseline |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 62 |
| Config Hash | c8fb25b3c8305ed8489f0b82ae21ac589cd3d3838465ae5501afdf2b7de57cfe |
| Artifacts Path | `tmp_compare\gradual_drift\adaptive_meta\experiments\gradual-drift-selector-adaptive-meta-baseline-20260428145532-7f6ea6d1` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.964797 |
| Success Rate | 1.000000 |
| Cumulative Reward | 57.887798 |
| Mean Window Variance | 0.001224 |
| Final Strategy | adaptive_meta |

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
experiment_name: gradual-drift-selector-adaptive_meta-baseline
seed: 62
mode: baseline
scenario:
  name: gradual_drift
  episodes: 60
  steps_per_episode: 20
  reward_noise_std: 0.0
  drift_episode: null
  drift_start_episode: 20
  drift_end_episode: 45
  fallback_patience: null
  tags:
  - drift
  - gradual
  description: Reward regime shifts gradually over a wide interval.
strategies:
- name: adaptive_meta
  parameters:
    temperature: 0.9
    evaluation_window: 24
  enabled: true
  compute_cost: 0.22
  description: null
meta_controller:
  window_size: 8
  min_samples: 5
  delta: 0.01
  lambda: 0.3
  switch_cost: 0.01
  utility_weights:
    reward_mean: 1.0
    reward_variance: 0.2
    compute_cost: 0.15
    switch_cost: 0.5
artifacts_root: tmp_compare\gradual_drift\adaptive_meta
tags:
- phase1
- gradual_drift
notes: null
```
