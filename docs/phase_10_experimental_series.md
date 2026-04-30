# Фаза 10. Експериментальні серії

Фаза 10 виконується раннером `Phase10ExperimentalSeriesRunner`, який формує серії `E1..E9` у каталозі `artifacts/phase10_experimental_series/`.

Для кожної серії зберігаються:
- `phase10_series_summary.json`
- `phase10_series_report.md`
- primary plot
- `phase10_switch_count.png`
- вкладені run/replay артефакти

Top-level індекс:
- `artifacts/phase10_experimental_series/phase10_suite_summary.json`
- `artifacts/phase10_experimental_series/phase10_suite_report.md`

## Склад серій

| Серія | Зміст | Тип | Обсяг |
| --- | --- | --- | ---: |
| `E1` | stationary control | seeded experiment suite | `n=5` |
| `E2` | abrupt drift | seeded experiment suite | `n=5` |
| `E3` | gradual drift | seeded experiment suite | `n=5` |
| `E4` | noisy reward | seeded experiment suite | `n=5` |
| `E5` | tempered reward shaping | benchmark profile suite | `n=3` |
| `E6` | drift-aware selector / H1 control | benchmark profile suite | `n=3` |
| `E7` | reproducibility | seeded experiment suite | `n=5` |
| `E8` | fallback insufficient data | seeded experiment suite | `n=5` |
| `E9` | baseline comparison | benchmark profile suite | `n=15` |

## Протокол виконання

### Seeded серії

- `E1`, `E2`, `E3`, `E4`, `E8`: seeds `41, 42, 43, 44, 45`
- `E7`: seed `12345`, повторено `5` разів

### Benchmark серії

Використані датасети:
- `Airlines`
- `Elec2`
- `InsectsRecurring`

Використані профілі:
- `E5`: `h2_tempered_drift`
- `E6`: `h1_drift_aware_v2`
- `E9`: `adaptive_meta_final`, `greedy_reward`, `h1_drift_aware_v2`, `h2_tempered_drift`, `hard_switch_lcb`

Фіксований benchmark-протокол:
- `max_samples = 256`
- `seed_protocol = deterministic_temporal_replay_no_rng`
- benchmark-серії інтерпретуються як deterministic replay, а не як випадкові multi-seed запуски

## Формат артефактів

### Seeded серії

Кожен рядок серії містить посилання на:
- `config.yaml`
- `metrics.csv`
- `decisions.csv`
- `report.md`
- `report.html`
- `reward_curve.png`
- `strategy_timeline.png`
- `utility_lcb.png`
- `versions.json`

### Benchmark серії

Кожен результат серії містить:
- `artifact_root_path`
- `config_path`
- `metrics.csv`
- `summary.json`
- `summary.md`
- `decisions.csv`
- `score_profile.png`

На рівні серії додатково фіксуються:
- `n`
- `seed_protocol`
- `delta_mean`
- `delta_std`
- `delta_ci95`
- `effect_size_d`
- `paired_sign_test_p_value`
- `benchmark_protocol`

## Ключові перевірки

- `E7` підтверджує відтворюваність:
  - `all_reward_means_identical = true`
  - `all_switch_counts_identical = true`
  - `all_final_strategies_identical = true`
- `E5`, `E6`, `E9` перегенеровані під одним фіксованим протоколом без змішування старих chunk-режимів
- top-level `phase10_suite_report.md` містить зведені таблиці для controlled і benchmark серій

## Поточний статус

Фаза 10 вважається завершеною, якщо:
- у `phase10_suite_summary.json` присутні всі `E1..E9`
- для кожної серії існують `phase10_series_summary.json` і `phase10_series_report.md`
- benchmark-серії мають однорідний `benchmark_protocol`
- phase-level звіт містить підсумкові таблиці та шляхи до артефактів
