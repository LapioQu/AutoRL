# Requirements Inventory

Working inventory of requirements from T3 with current status after the corrective phase 0-7 audit.

## Status Legend

| Status | Meaning |
| --- | --- |
| `tested` | Implemented and backed by automated tests or artifact-backed validation |
| `implemented` | Implemented but not yet covered by a dedicated requirement-level test |
| `partial` | Implemented only in part of the required scope |
| `deferred` | Explicitly not implemented yet in the current phase scope |

## Architecture Decisions

| ID | Decision | Status | Evidence |
| --- | --- | --- | --- |
| AD-01 | Modular monolith with `domain/application/infrastructure/interfaces` | tested | package structure, import tests |
| AD-02 | Domain isolated from presentation/storage concerns | tested | AST import contract test for `src/autorl/domain` |
| AD-03 | CLI uses application services, not domain/storage directly | tested | `src/autorl/interfaces/cli/app.py` |
| AD-04 | SQLite + filesystem artifacts for reproducibility | tested | storage integration tests |
| AD-05 | Standardized decision reasons | tested | `DecisionReason`, metacontroller tests |
| AD-06 | Controlled validation suite for non-stationary system validation | tested | `PhaseValidationRunner`, `artifacts/validation_suite_0_7/summary.md` |

## Use Cases

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| UC-01 | Create experiment | tested | config/orchestrator tests |
| UC-02 | Run experiment | tested | e2e CLI/orchestrator tests |
| UC-03 | Monitor execution in UI | tested | Streamlit phase 9 |
| UC-04 | View metrics in UI/API | tested | FastAPI + Streamlit |
| UC-05 | View decision log | tested | `decisions.csv`, report tests |
| UC-06 | Compare strategies | tested | compare API + Streamlit page |
| UC-07 | Generate report | tested | report integration tests |
| UC-08 | Export artifacts | tested in UI scope | Streamlit artifact index over real files |
| UC-09 | Rerun experiment | tested | CLI rerun test |
| UC-10 | Add new strategy | tested | strategy factory + extension guides + tests |
| UC-11 | Stop run | tested | FastAPI + Streamlit run monitor |
| UC-12 | Validate config | tested | CLI `validate-config` |

## Functional Requirements

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| FR-01 | Online + offline experiment modes | tested | CLI offline + API/UI monitoring |
| FR-02 | Metacontroller strategy switching | tested | evaluator/meta tests |
| FR-03 | Web monitoring interface | tested | Streamlit phase 9 |
| FR-04 | Decision latency <= 0.5s on CPU | tested | phase 4 latency smoke test |
| FR-05 | Persist configs/strategies/metrics history in DB | tested | storage tests |
| FR-06 | Reproducibility with fixed seeds | tested | reproducibility tests, validation suite |
| FR-07 | CPU-only operation | tested | full local runs on CPU |
| FR-08 | Accept experiment config file | tested | config loader tests |
| FR-09 | Configure environment/agent/strategies/window/seed | tested | config model tests |
| FR-10 | Automated execution from fixed configs | tested | orchestrator tests |
| FR-11 | Run in Gym-like supported environment | tested | `AdaptiveLearningEnv` tests |
| FR-12 | Control active learning strategy | tested | orchestrator + strategy tests |
| FR-13 | Strategy portfolio support | tested | strategy runtime tests |
| FR-14 | Add new strategies by developer | tested | extensible factory + extension guides + strategy tests |
| FR-15 | Collect episode metrics | tested | metrics tests |
| FR-16 | Aggregate window metrics | tested | rolling/window tests |
| FR-17 | Compute mean reward | tested | metrics tests |
| FR-18 | Compute reward variance/stability | tested | metrics/evaluator tests |
| FR-19 | Compute number of switches | tested | metrics tests |
| FR-20 | Compute recovery time | tested | metrics tests |
| FR-21 | Compute utility U | tested | evaluator tests |
| FR-22 | Compute LCB | tested | evaluator tests |
| FR-23 | Account for switch cost | tested | evaluator/meta tests |
| FR-24 | Account for delta threshold | tested | evaluator/meta tests |
| FR-25 | Support tempered reward / shaping line | tested | `TemperedRewardStrategy` tests |
| FR-26 | Produce Stay/Switch decisions | tested | metacontroller tests |
| FR-27 | Log reason for decision | tested | `DecisionReason`, report/CSV |
| FR-28 | Fallback on insufficient data | tested | metacontroller tests |
| FR-29 | Avoid switching on too-short/noisy fragments | tested | uncertainty/sample-threshold tests |
| FR-30 | Store episode log | tested | CSV/SQLite integration |
| FR-31 | Store metacontroller decision log | tested | CSV/SQLite integration |
| FR-32 | Store technical error/service log | tested | `events.log`, storage tests |
| FR-33 | Generate report artifacts | tested | reporting integration tests |
| FR-34 | User-visible access to decision log | tested | report/CLI/API |
| FR-35 | Compare baseline and adaptive strategies | tested | validation suite |
| FR-36 | Rerun from stored config + seed | tested | rerun test |
| FR-37 | Link rerun to original run | tested | `source_experiment_id`, export/status tests |
| FR-38 | API for create/run/stop/status/metrics/decisions/report | tested | FastAPI TestClient lifecycle tests |
| FR-39 | CLI run with config path | tested | CLI smoke |
| FR-40 | Streamlit UI | tested | `src/autorl/interfaces/ui/app.py`, `tests/test_ui_streamlit.py` |
| FR-41 | Show run list | tested | CLI `list` + `GET /experiments` |
| FR-42 | Show current active strategy | tested | `GET /experiments/{id}/status` |
| FR-43 | Show reward chart | tested | `reward_curve.png` |
| FR-44 | Show switch count | tested | report + API status/compare |
| FR-45 | Show decision journal | tested | report + `GET /experiments/{id}/decisions` |
| FR-46 | Export CSV/JSON/Markdown/HTML artifacts | tested | export CLI + HTML/JSON/zip tests |
| FR-47 | Support stationary/abrupt/gradual/noisy scenarios | tested | environment/config tests |
| FR-48 | Support repeated seed series | tested | validation suite `n=5` |
| FR-49 | Support fixed strategy baseline | tested | validation suite `fixed_*` runs |
| FR-50 | Support greedy/random/negative-control comparators | tested | greedy + random + negative-control implementations/tests |
| FR-51 | Support drift-aware comparator, not primary mechanism | tested | `DriftAwareStrategy`, validation inventory |
| FR-52 | Support uncertainty/multi-objective/tempered shaping line | tested | utility/LCB + tempered strategy + tempered replay profile |
| FR-53 | Generate reward/timeline/utility-LCB plots | tested | report plot tests |
| FR-54 | Generate result tables with p-value/CI/effect size where appropriate | tested | validation suite summary/report with CI, effect size, p-value |
| FR-55 | Provide operational documentation | tested | README + `docs/operations_manual.md` |
| FR-56 | Support `online-monitoring` and `offline-batch` modes | tested | CLI batch + API/UI monitor workflow |
| FR-57 | Explicit orchestrator state model | tested | `ExperimentStatus` + transition validation tests |
| FR-58 | Benchmark replay mode for H1/H2 | tested | profile-driven replay runner + CLI + tests |
| FR-59 | Candidate models for benchmark replay | tested | `build_candidate_model_registry(...)` + profile suite tests |
| FR-60 | Unified metric schema across UI/API/CSV/SQLite/reports | tested | Streamlit consumes the same persisted schema |
| FR-61 | Standardized Stay/Switch/fallback reason enum | tested | `DecisionReason`, DB/CSV/report |

## Non-Functional Requirements

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| NFR-01 | Local deployment | tested | local-only execution |
| NFR-02 | Python 3.11 + venv | tested | runtime/version contract test + operations manual |
| NFR-03 | CPU compatibility | tested | full test + suite runs |
| NFR-04 | Decision latency <= 0.5s | tested | phase 4 smoke test |
| NFR-05 | Memory <= 512 MB in performance test | tested | `tests/test_state_and_exports.py` memory smoke |
| NFR-06 | Seed reproducibility | tested | reproducibility tests |
| NFR-07 | Config snapshot persistence | tested | `config.yaml` |
| NFR-08 | Config hash persistence | tested | `config_hash.txt` |
| NFR-09 | Library version persistence | tested | `versions.json` |
| NFR-10 | Environment parameter persistence | tested | config snapshot |
| NFR-11 | Strategy list persistence | tested | config snapshot / DB |
| NFR-12 | Timestamp persistence | tested | DB rows and events |
| NFR-13 | Artifact path persistence | tested | `experiments.artifacts_path` |
| NFR-14 | Stay/Switch traceability | tested | decisions table/report |
| NFR-15 | Explainable decisions | tested | reason text + reason codes |
| NFR-16 | Modularity | tested | layer structure |
| NFR-17 | Strategy extensibility | tested | factory + strategy extension guide + tests |
| NFR-18 | Environment extensibility | tested | multiple replay environments + environment extension guide |
| NFR-19 | Reliable logging on failure | tested | partial log retention tests |
| NFR-20 | Partial logs survive crashes/errors | tested | artifact write error test |
| NFR-21 | File path control | tested | `PathGuard` tests |
| NFR-22 | Writes restricted to artifact roots | tested | `PathGuard` tests |
| NFR-23 | No personal data storage | tested | uploaded CSVs persisted as manifests/hashes only; no raw input storage |
| NFR-24 | No mandatory external DB server | tested | SQLite only |
| NFR-25 | No external data transfer | tested | local-only implementation |
| NFR-26 | UI must not contain domain logic | tested | Streamlit uses `ExperimentApiService` only |
| NFR-27 | Shared app services for API/CLI/UI | tested | CLI + API + UI share application services |
| NFR-28 | pytest + coverage support | tested | `pytest-cov` dependency + successful coverage run |
| NFR-29 | Git versioning | tested | initialized Git repository + contract test |
| NFR-30 | README operational documentation | tested | README + operations manual |
| NFR-31 | No final scientific conclusion from single run | tested | validation and benchmark suite reports include multi-run context/caution notes |
| NFR-32 | Final tables include `n`, seeds, mean, std/CI, caution | tested in current validation scope | validation suite summary |
| NFR-33 | Benchmark replay stores no personal identifiers | tested in current benchmark scope | replay suite artifacts contain only aggregate metrics and decision rows |
| NFR-34 | Reports exclude personal records/raw user trajectories | tested | dataset-lab reports/summaries exclude raw rows and forecast payloads |

## UI Acceptance Criteria

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| UI-AC-01 | Create experiment without editing code | tested | `tests/test_ui_streamlit.py`, `docs/ui_acceptance_checklist.md` |
| UI-AC-02 | Start experiment and see status | tested | `tests/test_ui_streamlit.py`, `docs/ui_acceptance_checklist.md` |
| UI-AC-03 | View reward/utility/LCB charts | tested | `Metrics Dashboard`, `utility_lcb.png` |
| UI-AC-04 | View active strategy timeline | tested | `Strategy Timeline` tab |
| UI-AC-05 | View Stay/Switch journal with reasons | tested | `Decision Journal` tab |
| UI-AC-06 | Compare baseline/adaptive | tested | `Compare Strategies` tab |
| UI-AC-07 | Export report and CSV from UI | tested in current scope | `Reports / Export` tab |
| UI-AC-08 | Rerun from previous config in UI | tested | `Run / Monitor` tab |

## API Endpoints

| Endpoint | Status | Evidence |
| --- | --- | --- |
| `POST /experiments` | tested | `tests/test_api_fastapi.py` |
| `POST /experiments/{id}/start` | tested | `tests/test_api_fastapi.py` |
| `POST /experiments/{id}/stop` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments/{id}` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments/{id}/status` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments/{id}/metrics` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments/{id}/decisions` | tested | `tests/test_api_fastapi.py` |
| `GET /experiments/{id}/report` | tested | `tests/test_api_fastapi.py` |
| `POST /experiments/{id}/rerun` | tested | `tests/test_api_fastapi.py` |
| `GET /scenarios` | tested | `tests/test_api_fastapi.py` |
| `GET /strategies` | tested | `tests/test_api_fastapi.py` |
| `GET /compare` | tested | `tests/test_api_fastapi.py` |

## CLI Commands

| Command | Status | Evidence |
| --- | --- | --- |
| `autorl validate-config --config ...` | tested | CLI smoke |
| `autorl run --config ...` | tested | CLI smoke |
| `autorl list` | tested | CLI smoke |
| `autorl report --experiment-id ...` | tested | CLI smoke |
| `autorl rerun --experiment-id ...` | tested | CLI smoke |
| `autorl validate-suite` | tested | CLI smoke |
| `autorl benchmark-elec2` | tested | CLI smoke with bounded sample replay |
| `autorl benchmark-suite` | tested | CLI smoke with bounded suite replay |
| `autorl run-suite --config ...` | tested | CLI smoke |
| `autorl status --experiment-id ...` | tested | CLI smoke |
| `autorl export --experiment-id ... --format zip` | tested | CLI smoke/export tests |

## Storage Elements

| Element | Status | Evidence |
| --- | --- | --- |
| SQLite `experiments` | tested | storage tests |
| SQLite `configs` | tested | storage tests |
| SQLite `episode_metrics` | tested | storage tests |
| SQLite `window_metrics` | tested | storage tests |
| SQLite `decisions` | tested | storage tests |
| SQLite `artifacts` | tested | storage tests |
| SQLite `events` | tested | storage tests |
| Artifact `config.yaml` | tested | storage tests |
| Artifact `config_hash.txt` | tested | storage tests |
| Artifact `versions.json` | tested | storage tests |
| Artifact `metrics.csv` | tested | storage/report tests |
| Artifact `window_metrics.csv` | tested | storage/report tests |
| Artifact `decisions.csv` | tested | storage/report tests |
| Artifact `events.log` | tested | storage tests |
| Artifact `report.md` | tested | report tests |
| Artifact `reward_curve.png` | tested | report tests |
| Artifact `strategy_timeline.png` | tested | report tests |
| Artifact `utility_lcb.png` | tested | report tests |

## System and Experimental Validation Items

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| SE-01 | Stationary control validation | tested | stationary e2e + LCB no-switch replay test |
| SE-02 | Abrupt drift system validation | tested | validation suite |
| SE-03 | Gradual drift system validation | tested | validation suite |
| SE-04 | Noisy reward false-switch validation | tested | LCB vs recent-leader false-switch replay test |
| SE-05 | Fallback validation | tested | fallback tests |
| SE-06 | Rerun validation | tested | rerun/reproducibility tests |
| SE-07 | UI workflow validation | tested | `tests/test_ui_streamlit.py` |
| EXP-01 | Global baseline suite | tested | benchmark profile suite runner + comparator suite smoke |
| EXP-02 | H1 v2 drift-aware contextual selection | tested | `h1_drift_aware_v2` profile runner smoke |
| EXP-03 | H2 search | tested | `h2_search` profile runner smoke |
| EXP-04 | H2 tempered | tested | `h2_tempered_*` profile runner smoke |
| EXP-05 | Adaptive Meta vs fixed/greedy/drift-aware/lcb/tempered | tested | explicit comparator profiles + benchmark suite smoke |

## Documentation Deliverables

| ID | Short Description | Status | Evidence |
| --- | --- | --- | --- |
| DOC-01 | Use Case Diagram | tested | `docs/doc_01_use_case_diagram.md` |
| DOC-02 | DFD Level 0 | tested | `docs/doc_02_dfd_level_0.md` |
| DOC-03 | Component Diagram | tested | `docs/doc_03_component_diagram.md` |
| DOC-04 | Sequence Diagram Stay/Switch | tested | `docs/doc_04_sequence_stay_switch.md` |
| DOC-05 | State Machine Diagram | tested | `docs/doc_05_state_machine.md` |
| DOC-06 | ER Diagram / SQL Schema | tested | `docs/doc_06_er_schema.md` |
| DOC-07 | Deployment Diagram | tested | `docs/doc_07_deployment_diagram.md` |
| DOC-08 | Requirements Traceability Matrix | tested | `docs/requirements_traceability.md` |
| DOC-09 | MoSCoW Requirements Table | tested | `docs/doc_09_moscow_requirements.md` |
| DOC-10 | Operational Instruction | tested | `docs/doc_10_operational_instruction.md`, `docs/operations_manual.md` |

## Current Audit Conclusion

The current implemented scope is sufficient to claim:

- controlled system validation of the adaptive core;
- reproducible artifact-backed runs and rerun lineage;
- API, CLI, UI, export, and artifact persistence closure;
- LCB-based switching validated on stationary, noisy, and non-stationary replay settings;
- benchmark replay and H1/H2 profile execution over the required candidate model registry;
- privacy-safe dataset-lab persistence without raw uploaded input storage.
- full documentation package for Phase 11, including traceability, test protocol, diagrams, and operational instructions.

The remaining work after this inventory is iterative product/research refinement, not an uncovered T3 requirement from the current scope.
