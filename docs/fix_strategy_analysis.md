# Fix Strategy Analysis

This note records the concrete engineering conclusion from the replay diagnostics:

> What change is most likely to move the system above the current `best fixed` baselines?

## Tested Candidates

### 1. Current controller

The current controller is:

- hard `Stay/Switch`
- LCB-threshold based
- strongly blocked by `high_uncertainty`

Observed issue:

- on chaotic streams such as `Elec2` and `Bikes`, it reacts too slowly and captures only a small fraction of the oracle gain.

### 2. Hedge-style expert weighting

An online full-information Hedge controller was added as an exploratory benchmark mode.

Result:

- `Elec2`: `-0.000927` vs best fixed
- `Bikes`: `-0.100351` vs best fixed
- `TrumpApproval`: `-0.004128` vs best fixed

Interpretation:

- this is not a good fit for the current action space;
- with discrete strategy execution, the weight-updating portfolio still accumulates too much regret before settling;
- therefore Hedge is not the recommended fix.

### 3. Recent-Leader / Champion-Challenger controller

A recent-leader controller was then implemented in replay mode with this rule:

- compute recent block performance for each stationary strategy;
- switch to the recent leader if its advantage exceeds a margin;
- add a short cooldown to reduce thrashing.

Best observed results from the tuned implementation:

| Dataset | Best Fixed | Recent-Leader Adaptive | Delta | Switches |
| --- | ---: | ---: | ---: | ---: |
| Elec2 | 0.916005 | 0.916645 | +0.000640 | 7 |
| Bikes | 0.676251 | 0.677979 | +0.001728 | 87 |
| TrumpApproval | 0.801432 | 0.800887 | -0.000545 | 1 |

Interpretation:

- on `Elec2`, recent-leader is already materially better than the current controller;
- on `Bikes`, it is much better than the current controller;
- on `TrumpApproval`, it almost matches the best fixed strategy and is far less harmful than the current controller.

## Engineering Conclusion

The most credible fix is:

1. replace or augment the current uncertainty-heavy hard-switch controller with a recent-leader champion-challenger controller;
2. keep a minimum margin and short cooldown, but remove the current aggressive `high_uncertainty` blocking behavior for replay-mode strategy selection;
3. warm-start from the best strategy in an initial calibration window instead of a weak fixed default.

In practical terms, the current system is not failing because it lacks a sophisticated enough regret algorithm.
It is failing because it is too conservative and because it starts from poor incumbents.

## Recommended Next Implementation

The next controller variant to implement in the main system should be:

- `recent_leader_meta`

with:

- warmup leader selection
- rolling lookback over the last `k` evaluation blocks
- advantage margin
- cooldown after switch
- optional incumbent floor so the controller does not move into clearly dominated strategies

This is the highest-signal path currently supported by the real-stream evidence.
