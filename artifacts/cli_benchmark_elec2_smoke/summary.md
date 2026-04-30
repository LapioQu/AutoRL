# Real-Stream Benchmark Replay

- dataset: `Elec2`
- score_name: `accuracy`
- policy_name: `hard_switch_lcb`
- samples: `256`
- source: Real NSW electricity market stream replayed in temporal order; target is whether the electricity price goes up or down.
- source_url: `https://maxhalford.github.io/files/datasets/electricity.zip`
- start_strategy: `sgd_lr_1_0`
- final_strategy: `sgd_lr_1_0`
- switch_count: `0`

## Score Summary

| Mode | Score |
| --- | ---: |
| adaptive | 0.925781 |
| sgd_lr_0_1 | 0.867188 |
| sgd_lr_0_5 | 0.921875 |
| sgd_lr_1_0 | 0.925781 |

- best_fixed_strategy: `sgd_lr_1_0`
- best_fixed_score: `0.925781`
- adaptive_delta_vs_best_fixed: `0.000000`
- block_delta_mean: `0.000000`
- block_delta_ci95: `0.000000`
- block_count: `2`

## Decisions

| Sample | Action | Current | Candidate | Margin | Threshold | Reason Code |
| ---: | --- | --- | --- | ---: | ---: | --- |
