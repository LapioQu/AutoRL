# Phase 0-7 Traceability

Historical phase-scope snapshot. Some rows below reflect the state at the end of the phase 0-7 audit only.
For the final cross-phase closure status, use [requirements_inventory.md](/E:/dipproj/docs/requirements_inventory.md).

This is the working traceability matrix for the implemented scope through phase 7.
It is intentionally limited to the requirements and acceptance criteria that are already relevant before phases 8-11.

| Requirement | Component | Verification | Artifact / Evidence | Status |
| --- | --- | --- | --- | --- |
| UC-01 Create experiment | `Config`, `ExperimentOrchestrator` | config tests, e2e run tests | generated experiment directories | tested |
| UC-02 Run experiment | `ExperimentOrchestrator` | `tests/test_orchestrator_cli.py` | `metrics.csv`, `decisions.csv`, `events.log` | tested |
| UC-05 View decision log | report generation, decision persistence | evaluator/meta tests, report tests | `decisions.csv`, `report.md` | tested |
| UC-07 Generate report | `ExperimentReportBuilder` | report/plot integration tests | `report.md`, `reward_curve.png`, `utility_lcb.png` | tested |
| UC-09 Rerun experiment | `rerun_experiment()` | CLI rerun smoke test | rerun artifact directory | tested |
| UC-12 Validate config | `load_config`, CLI `validate-config` | config tests, CLI validation smoke | printed `config_hash`, validation command | tested |
| FR-02 Metacontroller | `Evaluator`, `MetaController` | evaluator/meta tests | decision rows with reason codes | tested |
| FR-05 Persist history in DB | `SQLiteRepository` | storage integration tests | `autorl.db` tables | tested |
| FR-06 Reproducibility by seed | config hash + rerun + suite | reproducibility tests, validation suite | `artifacts/validation_suite_0_7/...` | tested |
| FR-08 Config file input | `load_config()` | config model tests | YAML/JSON examples | tested |
| FR-10 Automated experiment execution | `ExperimentOrchestrator.run()` | e2e tests | experiment bundles | tested |
| FR-11 Controlled environment | `AdaptiveLearningEnv` | environment tests | scenario-specific metrics | tested |
| FR-13 Strategy portfolio | runtime strategy registry | strategy tests | runtime selections | tested |
| FR-14 Add new strategies | strategy factory by class/prefix | import/strategy tests | `build_runtime_strategy()` | partial |
| FR-15 Episode metrics | `MetricsCollector.record_episode()` | metrics tests | `metrics.csv`, SQLite rows | tested |
| FR-16 Window aggregation | `window_metrics()` | metrics tests | `window_metrics.csv` | tested |
| FR-21 Utility U | `Evaluator.compute_utility()` | evaluator tests | utility values in decisions/windows | tested |
| FR-22 LCB | `Evaluator.compute_lcb()` | evaluator tests | LCB values in decisions | tested |
| FR-23 Switch cost | evaluator/metacontroller | evaluator tests | decision threshold fields | tested |
| FR-24 Delta threshold | metacontroller | evaluator tests | decision threshold fields | tested |
| FR-25 Tempered reward line | `TemperedRewardStrategy` | strategy tests | runtime policy support | tested |
| FR-26 Stay/Switch decisions | `MetaController.decide()` | evaluator/meta tests | `decisions.csv` | tested |
| FR-27 Decision reason logging | `DecisionReason`, report/CSV | evaluator/meta tests | `reason_code`, `reason` fields | tested |
| FR-28 Insufficient-data fallback | `MetaController` | evaluator/meta tests | fallback decisions | tested |
| FR-29 Avoid noise-driven switches | uncertainty threshold + windows | evaluator/meta tests | controlled stay behavior | tested |
| FR-30 Episode log | repository/store | storage tests | `episode_metrics`, `metrics.csv` | tested |
| FR-31 Decision log | repository/store | storage/report tests | `decisions` table, `decisions.csv` | tested |
| FR-32 Technical log | repository/store | storage tests | `events.log`, `events` table | tested |
| FR-33 Report artifacts | reporting layer | report tests | markdown + PNG outputs | tested |
| FR-35 Baseline vs adaptive comparison | validation runner | validation tests and suite | `artifacts/validation_suite_0_7/summary.md` | tested |
| FR-36 Rerun from saved config and seed | `rerun_experiment()` | rerun tests | linked rerun artifacts | tested |
| FR-37 Link rerun to saved config | rerun uses stored config snapshot | CLI rerun smoke | source config path in artifact bundle | partial |
| FR-39 CLI config-based execution | CLI `run` | CLI smoke tests | `autorl run --config ...` | tested |
| FR-46 CSV/Markdown export | artifact store + reporting | report/storage tests | CSV + Markdown outputs | partial |
| FR-47 Scenario support | environment + configs | environment tests | stationary, abrupt, gradual, noisy, fallback examples | tested |
| FR-48 Multi-seed repeat series | validation runner | validation tests and suite | `summary.json` with 5 seeds | tested |
| FR-49 Fixed strategy baseline | fixed strategy factory | validation tests | `fixed_low`, `fixed_mid`, `fixed_high` suite runs | tested |
| FR-50 Comparator strategies | greedy/lcb/adaptive policies | strategy tests | runtime registry | partial |
| FR-51 Drift-aware comparator | `DriftAwareStrategy` | strategy tests | comparator policy support | tested |
| FR-52 Uncertainty / tempered reward line | evaluator + tempered strategy | strategy/evaluator tests | runtime support and reports | partial |
| FR-53 Reward/timeline/utility plots | reporting layer | report tests | `reward_curve.png`, `strategy_timeline.png`, `utility_lcb.png` | tested |
| FR-54 CI/effect size tables where relevant | validation runner | validation suite | `summary.md`, `summary.json` | partial |
| FR-56 Online/offline modes | CLI offline path only | audit review | CLI exists, API/UI pending | partial |
| FR-57 Orchestrator state model | status updates only | audit review | DB status transitions | partial |
| FR-60 Unified metric schema across outputs | shared models + repository/reporting | report/storage tests | common field names in CSV/SQLite/report | partial |
| FR-61 Standardized decision enum | `DecisionReason` | evaluator/meta/storage tests | reason codes in DB/CSV/report | tested |
| NFR-03 CPU-only | local Python + no GPU deps required | full pytest, validation suite | CPU execution only | tested |
| NFR-04 Decision latency <= 0.5s | metacontroller timing smoke | evaluator/meta performance test | phase 4 test suite | tested |
| NFR-06 Reproducibility | rerun and repeated seeds | reproducibility tests, validation suite | seed-backed artifacts | tested |
| NFR-07..NFR-13 Reproducibility metadata | config snapshot/hash/versions/artifact paths | storage tests | `config.yaml`, `config_hash.txt`, `versions.json` | tested |
| NFR-14 Traceability of Stay/Switch | decision records and reports | report/meta tests | `decisions.csv`, `report.md` | tested |
| NFR-16 Modularity | layered package structure | import tests, audit review | `src/autorl/{domain,application,infrastructure,interfaces}` | tested |
| NFR-19..NFR-22 Safe logging and path control | `PathGuard`, artifact store | storage tests | blocked escape paths, preserved partial logs | tested |
| NFR-27 Shared application services for CLI/API/UI | application layer present | audit review | CLI uses app services, API/UI pending | partial |
| NFR-31 No single-run scientific claim | validation suite with `n=5` | validation suite | `summary.md` warning note | partial |
| NFR-32 n/seed/mean/std/CI tables | validation runner | validation suite | `summary.md`, `summary.json` | tested |
| SE-02 Abrupt drift system validation | validation runner | validation suite | abrupt drift artifacts | tested |
| SE-03 Gradual drift system validation | validation runner | validation suite | gradual drift artifacts | tested |
| SE-05 Fallback system validation | environment/meta tests | fallback tests | fallback-triggered episode metrics | tested |
| SE-06 Rerun system validation | orchestrator/CLI | rerun tests | rerun artifacts | tested |
| EXP-05 Adaptive vs fixed comparison | validation runner | validation suite | phase 0-7 summary artifacts | partial |
| CLI `validate-config` | CLI app | CLI smoke test | command output with config hash | tested |
| CLI `run` | CLI app + orchestrator | CLI smoke test | experiment artifacts | tested |
| CLI `list` | CLI app + repository | CLI smoke test | experiment rows | tested |
| CLI `report` | CLI app + reporting | CLI smoke test | markdown report output | tested |
| CLI `rerun` | CLI app + orchestrator | CLI smoke test | rerun artifact bundle | tested |
| CLI `validate-suite` | CLI app + validation runner | CLI smoke test | suite summary paths | tested |
| SQLite `experiments/configs/episode_metrics/window_metrics/decisions/artifacts/events` | repository schema | storage tests | `autorl.db` | tested |
| Artifact files `config.yaml/config_hash.txt/versions.json/metrics.csv/window_metrics.csv/decisions.csv/events.log/report.md/*.png` | artifact store + reporting | storage/report tests | experiment artifact directories | tested |
