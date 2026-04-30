# AutoRL Experiment Report

## Experiment Summary

| Field | Value |
| --- | --- |
| Experiment ID | ui-ai-review-run-20260429070712-1f560ed2 |
| Experiment Name | ui-ai-review-run |
| Status | completed |
| Scenario | abrupt_drift |
| Seed | 42 |
| Config Hash | 63711e4cd7d8a043fac7ab47984126abf16207e5369b3a81939e231095092a12 |
| Artifacts Path | `E:\dipproj\artifacts\ui_external_ai_review\workspace\artifacts\experiments\ui-ai-review-run-20260429070712-1f560ed2` |

## Results Summary

| Metric | Value |
| --- | ---: |
| Episodes | 24 |
| Decisions | 19 |
| Switches | 0 |
| Fallback Decisions | 5 |
| Average Reward | 0.748740 |
| Success Rate | 0.500000 |
| Cumulative Reward | 17.969755 |
| Mean Window Variance | 0.010360 |
| Final Strategy | fixed |

## Plot Artifacts

- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`

## Stay/Switch Summary

| Evaluation | Action | Current | Candidate | Margin | Threshold | Reason |
| --- | --- | --- | --- | ---: | ---: | --- |
| 0 | stay | fixed | adaptive_meta | - | 0.060000 | insufficient_samples |
| 1 | stay | fixed | adaptive_meta | - | 0.060000 | insufficient_samples |
| 2 | stay | fixed | adaptive_meta | -0.006738 | 0.060000 | no_candidate_improvement |
| 3 | stay | fixed | adaptive_meta | -0.002255 | 0.060000 | no_candidate_improvement |
| 4 | stay | fixed | adaptive_meta | -0.000937 | 0.060000 | no_candidate_improvement |
| 5 | stay | fixed | adaptive_meta | -0.000389 | 0.060000 | no_candidate_improvement |
| 6 | stay | fixed | adaptive_meta | -0.000162 | 0.060000 | no_candidate_improvement |
| 7 | stay | fixed | adaptive_meta | -0.000067 | 0.060000 | no_candidate_improvement |
| 8 | stay | fixed | adaptive_meta | -0.000028 | 0.060000 | no_candidate_improvement |
| 9 | stay | fixed | adaptive_meta | -0.000012 | 0.060000 | no_candidate_improvement |
| 10 | stay | fixed | adaptive_meta | -0.000005 | 0.060000 | high_uncertainty |
| 11 | stay | fixed | adaptive_meta | -0.000002 | 0.060000 | high_uncertainty |
| 12 | stay | fixed | adaptive_meta | -0.000001 | 0.060000 | high_uncertainty |
| 13 | stay | fixed | adaptive_meta | -0.000001 | 0.060000 | no_candidate_improvement |
| 14 | stay | fixed | adaptive_meta | -0.000000 | 0.060000 | no_candidate_improvement |
| 15 | stay | fixed | adaptive_meta | -0.000000 | 0.060000 | no_candidate_improvement |
| 16 | stay | fixed | adaptive_meta | -0.000000 | 0.060000 | no_candidate_improvement |
| 17 | stay | fixed | adaptive_meta | -0.000000 | 0.060000 | no_candidate_improvement |
| 18 | stay | fixed | adaptive_meta | -0.000000 | 0.060000 | no_candidate_improvement |

## Config Snapshot

```yaml
schema_version: '1.0'
experiment_name: ui-ai-review-run
seed: 42
mode: adaptive
scenario:
  name: abrupt_drift
  episodes: 24
  steps_per_episode: 8
  reward_noise_std: 0.0
  drift_episode: 12
  drift_start_episode: null
  drift_end_episode: null
  fallback_patience: null
  tags:
  - ui
  - ai-review
  description: Run for external AI operations review.
strategies:
- name: fixed
  parameters:
    fixed_action_index: 0
  enabled: true
  compute_cost: 0.05
  description: null
- name: adaptive_meta
  parameters:
    temperature: 0.6
  enabled: true
  compute_cost: 0.2
  description: null
meta_controller:
  window_size: 6
  min_samples: 3
  delta: 0.01
  lambda: 0.0
  switch_cost: 0.05
  utility_weights:
    compute_cost: 0.0
    reward_mean: 1.0
    reward_variance: 0.0
    switch_cost: 0.0
artifacts_root: E:\dipproj\artifacts\ui_external_ai_review\workspace\artifacts
tags:
- ui
- ai-review
notes: Generated for external AI review.
```
