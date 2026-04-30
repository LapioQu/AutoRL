# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | gradual-drift-selector-20260428145525-54f3cafe |
| Experiment Name | gradual-drift-selector |
| Status | completed |
| Scenario | gradual_drift |
| Seed | 62 |
| Config Hash | 9917797c4a647d589225172b6848807e90ba5ef4202ee02a0bbb0b7c6be3c7d0 |
| Artifacts Path | `tmp_compare\gradual_drift\experiments\gradual-drift-selector-20260428145525-54f3cafe` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 60 |
| Decisions | 53 |
| Switches | 2 |
| Fallback Decisions | 28 |
| Average Reward | 0.778460 |
| Success Rate | 0.683333 |
| Cumulative Reward | 46.707598 |
| Mean Window Variance | 0.005936 |
| Final Strategy | tempered_reward |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | tempered_reward | adaptive_meta | - | 0.020000 | insufficient_samples |
| 1 | stay | tempered_reward | adaptive_meta | - | 0.020000 | insufficient_samples |
| 2 | stay | tempered_reward | adaptive_meta | - | 0.020000 | insufficient_samples |
| 3 | stay | tempered_reward | adaptive_meta | - | 0.020000 | insufficient_samples |
| 4 | switch | tempered_reward | adaptive_meta | 0.171508 | 0.020000 | switch_advantage |
| 5 | stay | adaptive_meta | tempered_reward | -0.187131 | 0.020000 | no_candidate_improvement |
| 6 | stay | adaptive_meta | tempered_reward | -0.188941 | 0.020000 | no_candidate_improvement |
| 7 | stay | adaptive_meta | tempered_reward | -0.189655 | 0.020000 | no_candidate_improvement |
| 8 | stay | adaptive_meta | tempered_reward | -0.188686 | 0.020000 | no_candidate_improvement |
| 9 | stay | adaptive_meta | tempered_reward | -0.186693 | 0.020000 | no_candidate_improvement |
| 10 | stay | adaptive_meta | tempered_reward | -0.184670 | 0.020000 | no_candidate_improvement |
| 11 | stay | adaptive_meta | tempered_reward | -0.181903 | 0.020000 | no_candidate_improvement |
| 12 | stay | adaptive_meta | tempered_reward | -0.178138 | 0.020000 | no_candidate_improvement |
| 13 | stay | adaptive_meta | tempered_reward | -0.174951 | 0.020000 | no_candidate_improvement |
| 14 | stay | adaptive_meta | tempered_reward | -0.173831 | 0.020000 | no_candidate_improvement |
| 15 | stay | adaptive_meta | tempered_reward | -0.170100 | 0.020000 | no_candidate_improvement |
| 16 | stay | adaptive_meta | tempered_reward | -0.166103 | 0.020000 | no_candidate_improvement |
| 17 | stay | adaptive_meta | tempered_reward | -0.165953 | 0.020000 | no_candidate_improvement |
| 18 | stay | adaptive_meta | tempered_reward | -0.166725 | 0.020000 | no_candidate_improvement |
| 19 | stay | adaptive_meta | tempered_reward | -0.164761 | 0.020000 | no_candidate_improvement |

_Showing first 20 of 53 decisions._

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: gradual-drift-selector
seed: 62
mode: adaptive
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
artifacts_root: tmp_compare\gradual_drift
tags:
- phase1
- gradual_drift
notes: null
```
