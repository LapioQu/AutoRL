# Nonstationary Dataset Candidates

This note records the next dataset candidates that are most favorable for the AutoRL nonstationary self-learning system.

The selection criterion is not just "a stream exists", but rather:

- the environment changes over time;
- a fixed update strategy is likely to become suboptimal;
- multiple stationary learners or update policies can plausibly take turns being locally best;
- the task is available from an official source and is practical to replay in our benchmark stack.

## Highest-Priority Candidates

| Dataset | Task | Why it fits AutoRL | Source |
| --- | --- | --- | --- |
| `Insects incremental_reoccurring_balanced` | multi-class classification | Explicit recurring concept drift benchmark; designed for drift evaluation and likely to require frequent switches between locally strong stationary strategies. It is now accessible through the official USP DS Repository fallback loader. | River: https://riverml.xyz/dev/api/datasets/Insects/ and USP DS Repository: https://sites.google.com/view/uspdsrepository |
| `Gas Sensor Array Drift` | classification | Real 36-month sensor drift; the dataset exists specifically to develop strategies that cope with sensor/concept drift over time. | UCI: https://archive.ics.uci.edu/dataset/224/gas |
| `Gas Sensor Array Drift at Different Concentrations` | classification / regression | Same real long-horizon drift setting, but with concentration information, which makes it useful for both classification and regression-style replay. | UCI: https://archive.ics.uci.edu/dataset/270/gas+sensor+array+drift+dataset+at+different+concentrations |
| `Airlines` | binary classification | Delay prediction is operationally nonstationary because carriers, airports, schedules, congestion, weather, and recovery dynamics shift over time. | MOA: https://moa.cms.waikato.ac.nz/datasets/ and BTS raw source: https://www.transtats.bts.gov/OT_Delay/ |
| `WebTraffic` | regression / forecasting | The official task description already points to anomalous events, missing values, and multi-model selection; this is a direct fit for our strategy-selection controller. | River: https://riverml.xyz/dev/api/datasets/WebTraffic/ |

## Secondary Candidates

| Dataset | Task | Why it is still useful | Source |
| --- | --- | --- | --- |
| `WaterFlow` | regression / forecasting | Contains explicit anomalous segments and regime changes due to losses, maintenance, and pumping operations. | River: https://riverml.xyz/0.21.2/api/datasets/WaterFlow/ |
| `Taxis` | regression | Real urban mobility stream with demand and traffic regime shifts; useful once the strategy portfolio is richer than just learning-rate variants. | River: https://riverml.xyz/dev/api/datasets/Taxis/ |
| `TREC07` | binary classification | Chronologically ordered spam filtering stream; campaign drift can make fixed policies stale over time. | River: https://riverml.xyz/dev/api/datasets/TREC07/ |

## Recommended Benchmark Order

1. `Insects incremental_reoccurring_balanced`
2. `Gas Sensor Array Drift`
3. `WebTraffic`
4. `Airlines`

Reasoning:

- `Insects` is the fastest way to stress-test frequent switching.
- `Gas Sensor Drift` is the cleanest real-world drift dataset for proving that fixed strategies age.
- `WebTraffic` is the most natural regression-style candidate for our current replay architecture because anomalies and multi-model behavior are explicit in the official description.
- `Airlines` is the strongest production-like classification case, but its ingestion and preprocessing are heavier.

## What This Means For The System

The current evidence suggests two separate truths:

- some streams are already chaotic enough and expose controller weakness (`Elec2`, `Bikes`);
- we still need more favorable datasets where the local leader changes often enough for strategy switching to matter even more.

The best next additions are therefore:

- one recurring-drift benchmark: `Insects incremental_reoccurring_balanced`
- one real long-horizon drift benchmark: `Gas Sensor Array Drift`
- one real anomalous forecasting benchmark: `WebTraffic`
