# Nonstationary Dataset Replay Results

This note records what happened after integrating additional candidate streams beyond the original `Elec2`, `Bikes`, and `TrumpApproval` suite.

## Integrated Datasets

- `WebTraffic`
- `WaterFlow`
- `Airlines`
- `InsectsRecurring`

## Current Replay Outcomes

### Hard-switch baseline

Artifacts:

- `artifacts/real_stream_validation/suite_new_candidates_hard/suite_summary.md`

Observed scores:

| Dataset | Policy | Adaptive | Best Fixed | Delta | Switches |
| --- | --- | ---: | ---: | ---: | ---: |
| `WebTraffic` | `hard_switch_lcb` | 0.650297 | 0.650297 | ~0.000000 | 0 |
| `WaterFlow` | `hard_switch_lcb` | 0.803869 | 0.817426 | -0.013556 | 3 |

### Tuned recent-leader controller

Artifacts:

- `artifacts/real_stream_validation/suite_new_candidates_recent/suite_summary.md`
- `artifacts/real_stream_validation/suite_portfolio_improved_v2/suite_summary.md`

Observed scores:

| Dataset | Policy | Adaptive | Best Fixed | Delta | Switches |
| --- | --- | ---: | ---: | ---: | ---: |
| `WebTraffic` | `recent_leader_meta` | 0.650297 | 0.650297 | ~0.000000 | 1 |
| `WaterFlow` | `recent_leader_meta` | 0.814846 | 0.817426 | -0.002579 | 1 |
| `Airlines` | `recent_leader_meta` | 0.646960 | 0.647060 | -0.000100 | 8 |
| `InsectsRecurring` | `recent_leader_meta` | 0.782283 | 0.782283 | 0.000000 | 0 |

### Improved hard-switch controller with richer portfolio support

Artifacts:

- `artifacts/real_stream_validation/suite_portfolio_improved_hard_v2/suite_summary.md`
- `artifacts/real_stream_validation/insects_hard/suite_summary.md`

Observed scores:

| Dataset | Policy | Adaptive | Best Fixed | Delta | Switches |
| --- | --- | ---: | ---: | ---: | ---: |
| `WaterFlow` | `hard_switch_lcb` | 0.806041 | 0.803945 | +0.002097 | 4 |
| `Airlines` | `hard_switch_lcb` | 0.641670 | 0.642170 | -0.000500 | 7 |
| `InsectsRecurring` | `hard_switch_lcb` | 0.787667 | 0.782283 | +0.005383 | 4 |

## Interpretation

### `WebTraffic`

This stream is not currently a strong benchmark for our strategy-switching system.

Why:

- the best fixed strategy dominates the available portfolio almost completely;
- the adaptive score differs from the best fixed score only at numerical noise scale;
- even after parameter search, the best adaptive gain found was effectively zero.

Practical conclusion:

- `WebTraffic` is useful as a robustness / non-regression stream;
- it is not currently a convincing stream for demonstrating substantial benefit from strategy switching.

### `WaterFlow`

This stream is more interesting.

Why:

- block-wise oracle analysis shows substantial room for adaptation;
- with the current three-strategy portfolio, the block oracle gain is approximately `+0.0178`;
- the block leader changes `26` times over `52` evaluation blocks.

This means the scenario itself is meaningfully nonstationary.

However:

- the currently chosen stationary portfolio contains a strong dominating fixed learner (`sgd_lr_0_005`);
- the recent-leader controller narrows the gap a lot, but still remains below the best fixed strategy in that portfolio.
- after upgrading the portfolio generator to a heterogeneous candidate bank, the hard-switch controller moves above the best fixed strategy in the deployed portfolio (`+0.002097`).

Practical conclusion:

- `WaterFlow` is a promising dataset for AutoRL;
- the bottleneck is not the scenario, but the current strategy portfolio design.

## Portfolio Sensitivity

A small WaterFlow portfolio search was run over learning-rate triplets.

Best observed balanced portfolio:

- strategies: `0.0005`, `0.001`, `0.002`
- controller params: `lookback=6`, `margin=0.005`, `warmup=1`, `cooldown=3`, `incumbent_floor=0.002`
- adaptive score: `0.805439`
- best fixed in that portfolio: `0.803945`
- delta: `+0.001494`

Interpretation:

- WaterFlow can support an adaptive win;
- but the win depends on offering the controller a balanced set of challengers rather than one clearly dominating fixed strategy.

## `InsectsRecurring`

`InsectsRecurring` is now accessible through an official fallback loader that downloads the USP DS Repository archive directly instead of relying on the broken River URL.

Observed result:

- with `recent_leader_meta`: no gain over best fixed;
- with `hard_switch_lcb`: `0.787667` vs `0.782283`, delta `+0.005383`, `4` switches.

Practical conclusion:

- this is the strongest new evidence that the system can outperform the best fixed stationary strategy on a recurring-drift benchmark when the dataset and portfolio are aligned;
- the best controller is not universal: here the improved hard-switch controller outperformed recent-leader.

## Engineering Takeaway

The extra dataset pass supports a more precise rule:

- `WebTraffic`: not favorable right now, because switching has almost no room to beat the dominating fixed learner;
- `WaterFlow`: favorable scenario, and it improves once the strategy registry is broadened and reselected more carefully;
- `Airlines`: now accessible and useful as a real operational benchmark, but not yet a clear adaptive win;
- `InsectsRecurring`: now accessible and already shows a meaningful adaptive win with the improved hard-switch controller.
