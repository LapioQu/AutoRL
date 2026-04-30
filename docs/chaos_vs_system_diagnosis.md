# Chaos vs System Diagnosis

This note answers one specific question:

> If the adaptive system does not strongly beat fixed strategies, is the problem that the scenario is not chaotic enough, or that the current AutoRL system is still underdeveloped?

The diagnosis below uses the current real-stream suite results from:

- `artifacts/real_stream_validation/suite/elec2`
- `artifacts/real_stream_validation/suite/bikes`
- `artifacts/real_stream_validation/suite/trump_approval`

## Method

For each dataset, the diagnosis uses four signals:

1. `leader_changes`
   block-wise number of changes in the best fixed strategy across the stream.
2. `oracle_gain`
   how much a block-wise oracle switching between the existing fixed strategies would outperform the best single fixed strategy.
3. `adaptive_capture`
   what fraction of that oracle gain the current adaptive controller actually captures.
4. decision reason distribution
   how often the current controller stays because of `high_uncertainty` or `no_candidate_improvement`.

Interpretation:

- if `leader_changes` and `oracle_gain` are both small, then the scenario does not offer much room for adaptive switching;
- if `leader_changes` and `oracle_gain` are large, but `adaptive_capture` is small, then the current system is underdeveloped for that scenario;
- if one fixed strategy dominates almost all blocks, then adaptive overhead is likely to hurt rather than help.

## Results

| Dataset | Best Fixed | Adaptive | Delta | Oracle Gain | Adaptive Capture | Leader Changes | Blocks | Switches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Elec2 | 0.916005 | 0.916159 | +0.000154 | 0.006908 | 0.022 | 178 | 354 | 5 |
| Bikes | 0.676251 | 0.677074 | +0.000823 | 0.004188 | 0.196 | 134 | 312 | 1 |
| TrumpApproval | 0.801432 | 0.783516 | -0.017916 | 0.002657 | -6.744 | 10 | 31 | 1 |

Decision reason counts:

- `Elec2`: `no_candidate_improvement=227`, `high_uncertainty=119`, `switch_advantage=5`
- `Bikes`: `no_candidate_improvement=69`, `high_uncertainty=240`, `switch_advantage=1`
- `TrumpApproval`: `no_candidate_improvement=7`, `high_uncertainty=21`, `switch_advantage=1`

## Diagnosis by Dataset

### Elec2

- This scenario is chaotic enough for adaptive switching.
- Evidence:
  - `178` leader changes over `354` blocks is high.
  - Oracle gain over the best fixed strategy is `+0.006908`, which is much larger than the achieved adaptive gain `+0.000154`.
- Current adaptive behavior is underreactive:
  - only `5` switches;
  - captures only about `2.2%` of the gain theoretically available from the current fixed portfolio.
- Main diagnosis:
  - the scenario is not the bottleneck;
  - the controller and/or strategy registry are underdeveloped.

### Bikes

- This scenario is also chaotic enough.
- Evidence:
  - `134` leader changes over `312` blocks;
  - oracle gain `+0.004188` is materially larger than adaptive gain `+0.000823`.
- The controller is even more conservative here than on Elec2:
  - only `1` switch;
  - `240` decisions were blocked by `high_uncertainty`.
- Main diagnosis:
  - the system is too uncertainty-averse for this stream;
  - again, the problem is not lack of chaos, but insufficient switching capability and a narrow strategy registry.

### TrumpApproval

- This scenario is not a strong fit for the current adaptive system.
- Evidence:
  - oracle gain is only `+0.002657`, so even perfect switching across the current portfolio would not buy much over the best fixed strategy;
  - one fixed strategy (`sgd_lr_0_05`) dominates most blocks.
- The adaptive system starts from a weaker strategy, switches once, and still ends below the best fixed baseline.
- Main diagnosis:
  - here the scenario/portfolio combination does not justify a metacontroller very well;
  - this dataset is better interpreted as a case where a strong stationary strategy is already enough.

## Overall Answer

The answer is mixed, but not ambiguous:

- for `Elec2` and `Bikes`, the scenario is already chaotic enough;
  the main bottleneck is the current AutoRL system;
- for `TrumpApproval`, the scenario is not chaotic enough, and the current portfolio contains a nearly dominant fixed strategy, so adaptive switching is not the right lever there.

In other words:

> The present system is underdeveloped relative to the amount of non-stationarity already present in Elec2 and Bikes.

and also:

> Not every real temporal dataset is a good target for adaptive strategy selection; TrumpApproval currently behaves more like a case where a strong fixed learner is sufficient.

## What This Implies Technically

The next improvement priority is not merely “find a more chaotic dataset”.

The evidence says we need both:

1. more chaotic datasets where adaptive switching should matter even more;
2. a stronger system that can actually exploit such chaos.

## Immediate Recommendations

1. Expand the strategy registry beyond learning-rate variants of one model.
2. Reduce excessive `high_uncertainty` blocking or redesign the uncertainty rule.
3. Add better warm-start / early-model-selection logic so adaptive runs do not begin from a weak default.
4. Add datasets such as `Gas Sensor Array Drift` and `INSECTS incremental_reoccurring` for stronger drift stress tests.
