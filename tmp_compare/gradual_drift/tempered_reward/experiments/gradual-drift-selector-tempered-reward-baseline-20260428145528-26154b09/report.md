# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | gradual-drift-selector-tempered-reward-baseline-20260428145528-26154b09 |
| Experiment Name | gradual-drift-selector-tempered_reward-baseline |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 62 |
| Config Hash | 9e68683586e288b3327eba53a8f59756f0c2b875054be0bd3445dcea834d0543 |
| Artifacts Path | `tmp_compare\gradual_drift\tempered_reward\experiments\gradual-drift-selector-tempered-reward-baseline-20260428145528-26154b09` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 0 |
| Switches | 0 |
| Fallback Decisions | 0 |
| Average Reward | 0.988797 |
| Success Rate | 1.000000 |
| Cumulative Reward | 59.327798 |
| Mean Window Variance | 0.001224 |
| Final Strategy | tempered_reward |

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
experiment_name: gradual-drift-selector-tempered_reward-baseline
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
- name: tempered_reward
  parameters:
    temperature: 0.7
    decay: 0.98
  enabled: true
  compute_cost: 0.1
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
artifacts_root: tmp_compare\gradual_drift\tempered_reward
tags:
- phase1
- gradual_drift
notes: null
```
