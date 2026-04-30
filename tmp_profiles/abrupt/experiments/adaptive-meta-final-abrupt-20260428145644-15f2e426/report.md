# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | adaptive-meta-final-abrupt-20260428145644-15f2e426 |
| Experiment Name | adaptive-meta-final-abrupt |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 42 |
| Config Hash | 76ff6cdcb498c8f80545d85338f6ca15f891e01780c62de61d3d33ed474aff65 |
| Artifacts Path | `tmp_profiles\abrupt\experiments\adaptive-meta-final-abrupt-20260428145644-15f2e426` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 80 |
| Decisions | 73 |
| Switches | 2 |
| Fallback Decisions | 14 |
| Average Reward | 1.049048 |
| Success Rate | 1.000000 |
| Cumulative Reward | 83.923836 |
| Mean Window Variance | 0.003770 |
| Final Strategy | fixed_high |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 1 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 2 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 3 | stay | fixed_low | fixed_mid | - | 0.020000 | insufficient_samples |
| 4 | switch | fixed_low | fixed_mid | 0.058949 | 0.020000 | switch_advantage |
| 5 | stay | fixed_mid | adaptive_meta_final | -0.007824 | 0.020000 | no_candidate_improvement |
| 6 | stay | fixed_mid | adaptive_meta_final | -0.007622 | 0.020000 | no_candidate_improvement |
| 7 | stay | fixed_mid | adaptive_meta_final | -0.007602 | 0.020000 | no_candidate_improvement |
| 8 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 9 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 10 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 11 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 12 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 13 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 14 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 15 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 16 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 17 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 18 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |
| 19 | stay | fixed_mid | adaptive_meta_final | -0.007600 | 0.020000 | no_candidate_improvement |

_Showing first 20 of 73 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: adaptive-meta-final-abrupt
seed: 42
mode: adaptive
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
- name: fixed_mid
  parameters:
    fixed_action_index: 1
  enabled: true
  compute_cost: 0.05
  description: null
- name: fixed_high
  parameters:
    fixed_action_index: 2
  enabled: true
  compute_cost: 0.07
  description: null
- name: adaptive_meta_final
  parameters:
    reward_weight: 0.25
    success_weight: 0.2
    fit_weight: 0.4
    recency_weight: 0.2
    cost_weight: 0.1
  enabled: true
  compute_cost: 0.12
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
artifacts_root: tmp_profiles/abrupt
tags: []
notes: null
```
