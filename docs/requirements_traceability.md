# Requirements Traceability

Final Phase 11 traceability matrix required by T3. This matrix covers all required groups: UC, FR, NFR, UI-AC, API endpoints, CLI commands, SQLite tables and artifact files, SE, EXP, and DOC deliverables.

| Group | ID / Element | Component | Test or Verification | Artifact Result | Status |
| --- | --- | --- | --- | --- | --- |
| Architecture Decisions | AD-01 | Project architecture and layer boundaries | package structure, import tests | package structure, import tests | tested |
| Architecture Decisions | AD-02 | Project architecture and layer boundaries | AST import contract test for `src/autorl/domain` | src/autorl/domain | tested |
| Architecture Decisions | AD-03 | Project architecture and layer boundaries | `src/autorl/interfaces/cli/app.py` | src/autorl/interfaces/cli/app.py | tested |
| Architecture Decisions | AD-04 | Project architecture and layer boundaries | storage integration tests | storage integration tests | tested |
| Architecture Decisions | AD-05 | Project architecture and layer boundaries | `DecisionReason`, metacontroller tests | DecisionReason | tested |
| Architecture Decisions | AD-06 | Project architecture and layer boundaries | `PhaseValidationRunner`, `artifacts/validation_suite_0_7/summary.md` | PhaseValidationRunner; artifacts/validation_suite_0_7/summary.md | tested |
| Use Cases | UC-01 | Application services + CLI/API/UI interfaces | config/orchestrator tests | config/orchestrator tests | tested |
| Use Cases | UC-02 | Application services + CLI/API/UI interfaces | e2e CLI/orchestrator tests | e2e CLI/orchestrator tests | tested |
| Use Cases | UC-03 | Application services + CLI/API/UI interfaces | Streamlit phase 9 | Streamlit phase 9 | tested |
| Use Cases | UC-04 | Application services + CLI/API/UI interfaces | FastAPI + Streamlit | FastAPI + Streamlit | tested |
| Use Cases | UC-05 | Application services + CLI/API/UI interfaces | `decisions.csv`, report tests | decisions.csv | tested |
| Use Cases | UC-06 | Application services + CLI/API/UI interfaces | compare API + Streamlit page | compare API + Streamlit page | tested |
| Use Cases | UC-07 | Application services + CLI/API/UI interfaces | report integration tests | report integration tests | tested |
| Use Cases | UC-08 | Application services + CLI/API/UI interfaces | Streamlit artifact index over real files | Streamlit artifact index over real files | tested in UI scope |
| Use Cases | UC-09 | Application services + CLI/API/UI interfaces | CLI rerun test | CLI rerun test | tested |
| Use Cases | UC-10 | Application services + CLI/API/UI interfaces | strategy factory + extension guides + tests | strategy factory + extension guides + tests | tested |
| Use Cases | UC-11 | Application services + CLI/API/UI interfaces | FastAPI + Streamlit run monitor | FastAPI + Streamlit run monitor | tested |
| Use Cases | UC-12 | Application services + CLI/API/UI interfaces | CLI `validate-config` | validate-config | tested |
| Functional Requirements | FR-01 | FastAPI app + ExperimentApiService | CLI offline + API/UI monitoring | CLI offline + API/UI monitoring | tested |
| Functional Requirements | FR-02 | Domain strategies + Evaluator + MetaController | evaluator/meta tests | evaluator/meta tests | tested |
| Functional Requirements | FR-03 | Streamlit UI | Streamlit phase 9 | Streamlit phase 9 | tested |
| Functional Requirements | FR-04 | Application/domain runtime | phase 4 latency smoke test | phase 4 latency smoke test | tested |
| Functional Requirements | FR-05 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | storage tests | storage tests | tested |
| Functional Requirements | FR-06 | Streamlit UI | reproducibility tests, validation suite | reproducibility tests, validation suite | tested |
| Functional Requirements | FR-07 | Application/domain runtime | full local runs on CPU | full local runs on CPU | tested |
| Functional Requirements | FR-08 | Application/domain runtime | config loader tests | config loader tests | tested |
| Functional Requirements | FR-09 | Application/domain runtime | config model tests | config model tests | tested |
| Functional Requirements | FR-10 | Application/domain runtime | orchestrator tests | orchestrator tests | tested |
| Functional Requirements | FR-11 | Application/domain runtime | `AdaptiveLearningEnv` tests | AdaptiveLearningEnv | tested |
| Functional Requirements | FR-12 | Domain strategies + Evaluator + MetaController | orchestrator + strategy tests | orchestrator + strategy tests | tested |
| Functional Requirements | FR-13 | Domain strategies + Evaluator + MetaController | strategy runtime tests | strategy runtime tests | tested |
| Functional Requirements | FR-14 | Streamlit UI | extensible factory + extension guides + strategy tests | extensible factory + extension guides + strategy tests | tested |
| Functional Requirements | FR-15 | Application/domain runtime | metrics tests | metrics tests | tested |
| Functional Requirements | FR-16 | Application/domain runtime | rolling/window tests | rolling/window tests | tested |
| Functional Requirements | FR-17 | Application/domain runtime | metrics tests | metrics tests | tested |
| Functional Requirements | FR-18 | Domain strategies + Evaluator + MetaController | metrics/evaluator tests | metrics/evaluator tests | tested |
| Functional Requirements | FR-19 | Application/domain runtime | metrics tests | metrics tests | tested |
| Functional Requirements | FR-20 | Application/domain runtime | metrics tests | metrics tests | tested |
| Functional Requirements | FR-21 | Domain strategies + Evaluator + MetaController | evaluator tests | evaluator tests | tested |
| Functional Requirements | FR-22 | Domain strategies + Evaluator + MetaController | evaluator tests | evaluator tests | tested |
| Functional Requirements | FR-23 | Domain strategies + Evaluator + MetaController | evaluator/meta tests | evaluator/meta tests | tested |
| Functional Requirements | FR-24 | Domain strategies + Evaluator + MetaController | evaluator/meta tests | evaluator/meta tests | tested |
| Functional Requirements | FR-25 | Domain strategies + Evaluator + MetaController | `TemperedRewardStrategy` tests | TemperedRewardStrategy | tested |
| Functional Requirements | FR-26 | Domain strategies + Evaluator + MetaController | metacontroller tests | metacontroller tests | tested |
| Functional Requirements | FR-27 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | `DecisionReason`, report/CSV | DecisionReason | tested |
| Functional Requirements | FR-28 | Domain strategies + Evaluator + MetaController | metacontroller tests | metacontroller tests | tested |
| Functional Requirements | FR-29 | Application/domain runtime | uncertainty/sample-threshold tests | uncertainty/sample-threshold tests | tested |
| Functional Requirements | FR-30 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | CSV/SQLite integration | CSV/SQLite integration | tested |
| Functional Requirements | FR-31 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | CSV/SQLite integration | CSV/SQLite integration | tested |
| Functional Requirements | FR-32 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | `events.log`, storage tests | events.log | tested |
| Functional Requirements | FR-33 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | reporting integration tests | reporting integration tests | tested |
| Functional Requirements | FR-34 | FastAPI app + ExperimentApiService | report/CLI/API | report/CLI/API | tested |
| Functional Requirements | FR-35 | Streamlit UI | validation suite | validation suite | tested |
| Functional Requirements | FR-36 | Application/domain runtime | rerun test | rerun test | tested |
| Functional Requirements | FR-37 | Application/domain runtime | `source_experiment_id`, export/status tests | source_experiment_id | tested |
| Functional Requirements | FR-38 | FastAPI app + ExperimentApiService | FastAPI TestClient lifecycle tests | FastAPI TestClient lifecycle tests | tested |
| Functional Requirements | FR-39 | Application/domain runtime | CLI smoke | CLI smoke | tested |
| Functional Requirements | FR-40 | Streamlit UI | `src/autorl/interfaces/ui/app.py`, `tests/test_ui_streamlit.py` | src/autorl/interfaces/ui/app.py; tests/test_ui_streamlit.py | tested |
| Functional Requirements | FR-41 | Application/domain runtime | CLI `list` + `GET /experiments` | list; GET /experiments | tested |
| Functional Requirements | FR-42 | Application/domain runtime | `GET /experiments/{id}/status` | GET /experiments/{id}/status | tested |
| Functional Requirements | FR-43 | Application/domain runtime | `reward_curve.png` | reward_curve.png | tested |
| Functional Requirements | FR-44 | FastAPI app + ExperimentApiService | report + API status/compare | report + API status/compare | tested |
| Functional Requirements | FR-45 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | report + `GET /experiments/{id}/decisions` | GET /experiments/{id}/decisions | tested |
| Functional Requirements | FR-46 | Application/domain runtime | export CLI + HTML/JSON/zip tests | export CLI + HTML/JSON/zip tests | tested |
| Functional Requirements | FR-47 | Application/domain runtime | environment/config tests | environment/config tests | tested |
| Functional Requirements | FR-48 | Streamlit UI | validation suite `n=5` | n=5 | tested |
| Functional Requirements | FR-49 | Streamlit UI | validation suite `fixed_*` runs | fixed_* | tested |
| Functional Requirements | FR-50 | Application/domain runtime | greedy + random + negative-control implementations/tests | greedy + random + negative-control implementations/tests | tested |
| Functional Requirements | FR-51 | Domain strategies + Evaluator + MetaController | `DriftAwareStrategy`, validation inventory | DriftAwareStrategy | tested |
| Functional Requirements | FR-52 | Domain strategies + Evaluator + MetaController | utility/LCB + tempered strategy + tempered replay profile | utility/LCB + tempered strategy + tempered replay profile | tested |
| Functional Requirements | FR-53 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | report plot tests | report plot tests | tested |
| Functional Requirements | FR-54 | Streamlit UI | validation suite summary/report with CI, effect size, p-value | validation suite summary/report with CI, effect size, p-value | tested |
| Functional Requirements | FR-55 | Application/domain runtime | README + `docs/operations_manual.md` | docs/operations_manual.md | tested |
| Functional Requirements | FR-56 | FastAPI app + ExperimentApiService | CLI batch + API/UI monitor workflow | CLI batch + API/UI monitor workflow | tested |
| Functional Requirements | FR-57 | Application/domain runtime | `ExperimentStatus` + transition validation tests | ExperimentStatus | tested |
| Functional Requirements | FR-58 | Application/domain runtime | profile-driven replay runner + CLI + tests | profile-driven replay runner + CLI + tests | tested |
| Functional Requirements | FR-59 | Streamlit UI | `build_candidate_model_registry(...)` + profile suite tests | build_candidate_model_registry(...) | tested |
| Functional Requirements | FR-60 | Streamlit UI | Streamlit consumes the same persisted schema | Streamlit consumes the same persisted schema | tested |
| Functional Requirements | FR-61 | ExperimentOrchestrator + SQLiteRepository + ArtifactStore + Reporting | `DecisionReason`, DB/CSV/report | DecisionReason | tested |
| Non-Functional Requirements | NFR-01 | Cross-cutting runtime and process controls | local-only execution | local-only execution | tested |
| Non-Functional Requirements | NFR-02 | Documentation package | runtime/version contract test + operations manual | runtime/version contract test + operations manual | tested |
| Non-Functional Requirements | NFR-03 | Cross-cutting runtime and process controls | full test + suite runs | full test + suite runs | tested |
| Non-Functional Requirements | NFR-04 | Cross-cutting runtime and process controls | phase 4 smoke test | phase 4 smoke test | tested |
| Non-Functional Requirements | NFR-05 | Cross-cutting runtime and process controls | `tests/test_state_and_exports.py` memory smoke | tests/test_state_and_exports.py | tested |
| Non-Functional Requirements | NFR-06 | Cross-cutting runtime and process controls | reproducibility tests | reproducibility tests | tested |
| Non-Functional Requirements | NFR-07 | Cross-cutting runtime and process controls | `config.yaml` | config.yaml | tested |
| Non-Functional Requirements | NFR-08 | Cross-cutting runtime and process controls | `config_hash.txt` | config_hash.txt | tested |
| Non-Functional Requirements | NFR-09 | Cross-cutting runtime and process controls | `versions.json` | versions.json | tested |
| Non-Functional Requirements | NFR-10 | Cross-cutting runtime and process controls | config snapshot | config snapshot | tested |
| Non-Functional Requirements | NFR-11 | Cross-cutting runtime and process controls | config snapshot / DB | config snapshot / DB | tested |
| Non-Functional Requirements | NFR-12 | Cross-cutting runtime and process controls | DB rows and events | DB rows and events | tested |
| Non-Functional Requirements | NFR-13 | Infrastructure layer | `experiments.artifacts_path` | experiments.artifacts_path | tested |
| Non-Functional Requirements | NFR-14 | Cross-cutting runtime and process controls | decisions table/report | decisions table/report | tested |
| Non-Functional Requirements | NFR-15 | Cross-cutting runtime and process controls | reason text + reason codes | reason text + reason codes | tested |
| Non-Functional Requirements | NFR-16 | Cross-cutting runtime and process controls | layer structure | layer structure | tested |
| Non-Functional Requirements | NFR-17 | Cross-cutting runtime and process controls | factory + strategy extension guide + tests | factory + strategy extension guide + tests | tested |
| Non-Functional Requirements | NFR-18 | Cross-cutting runtime and process controls | multiple replay environments + environment extension guide | multiple replay environments + environment extension guide | tested |
| Non-Functional Requirements | NFR-19 | Cross-cutting runtime and process controls | partial log retention tests | partial log retention tests | tested |
| Non-Functional Requirements | NFR-20 | Infrastructure layer | artifact write error test | artifact write error test | tested |
| Non-Functional Requirements | NFR-21 | Infrastructure layer | `PathGuard` tests | PathGuard | tested |
| Non-Functional Requirements | NFR-22 | Infrastructure layer | `PathGuard` tests | PathGuard | tested |
| Non-Functional Requirements | NFR-23 | Cross-cutting runtime and process controls | uploaded CSVs persisted as manifests/hashes only; no raw input storage | uploaded CSVs persisted as manifests/hashes only; no raw input storage | tested |
| Non-Functional Requirements | NFR-24 | Infrastructure layer | SQLite only | SQLite only | tested |
| Non-Functional Requirements | NFR-25 | Cross-cutting runtime and process controls | local-only implementation | local-only implementation | tested |
| Non-Functional Requirements | NFR-26 | Cross-cutting runtime and process controls | Streamlit uses `ExperimentApiService` only | ExperimentApiService | tested |
| Non-Functional Requirements | NFR-27 | Cross-cutting runtime and process controls | CLI + API + UI share application services | CLI + API + UI share application services | tested |
| Non-Functional Requirements | NFR-28 | Cross-cutting runtime and process controls | `pytest-cov` dependency + successful coverage run | pytest-cov | tested |
| Non-Functional Requirements | NFR-29 | Cross-cutting runtime and process controls | initialized Git repository + contract test | initialized Git repository + contract test | tested |
| Non-Functional Requirements | NFR-30 | Documentation package | README + operations manual | README + operations manual | tested |
| Non-Functional Requirements | NFR-31 | Cross-cutting runtime and process controls | validation and benchmark suite reports include multi-run context/caution notes | validation and benchmark suite reports include multi-run context/caution notes | tested |
| Non-Functional Requirements | NFR-32 | Cross-cutting runtime and process controls | validation suite summary | validation suite summary | tested in current validation scope |
| Non-Functional Requirements | NFR-33 | Infrastructure layer | replay suite artifacts contain only aggregate metrics and decision rows | replay suite artifacts contain only aggregate metrics and decision rows | tested in current benchmark scope |
| Non-Functional Requirements | NFR-34 | Cross-cutting runtime and process controls | dataset-lab reports/summaries exclude raw rows and forecast payloads | dataset-lab reports/summaries exclude raw rows and forecast payloads | tested |
| UI Acceptance Criteria | UI-AC-01 | Streamlit UI + DatasetLabService + ExperimentApiService | `tests/test_ui_streamlit.py`, `docs/ui_acceptance_checklist.md` | tests/test_ui_streamlit.py; docs/ui_acceptance_checklist.md | tested |
| UI Acceptance Criteria | UI-AC-02 | Streamlit UI + DatasetLabService + ExperimentApiService | `tests/test_ui_streamlit.py`, `docs/ui_acceptance_checklist.md` | tests/test_ui_streamlit.py; docs/ui_acceptance_checklist.md | tested |
| UI Acceptance Criteria | UI-AC-03 | Streamlit UI + DatasetLabService + ExperimentApiService | `Metrics Dashboard`, `utility_lcb.png` | Metrics Dashboard; utility_lcb.png | tested |
| UI Acceptance Criteria | UI-AC-04 | Streamlit UI + DatasetLabService + ExperimentApiService | `Strategy Timeline` tab | Strategy Timeline | tested |
| UI Acceptance Criteria | UI-AC-05 | Streamlit UI + DatasetLabService + ExperimentApiService | `Decision Journal` tab | Decision Journal | tested |
| UI Acceptance Criteria | UI-AC-06 | Streamlit UI + DatasetLabService + ExperimentApiService | `Compare Strategies` tab | Compare Strategies | tested |
| UI Acceptance Criteria | UI-AC-07 | Streamlit UI + DatasetLabService + ExperimentApiService | `Reports / Export` tab | Reports / Export | tested in current scope |
| UI Acceptance Criteria | UI-AC-08 | Streamlit UI + DatasetLabService + ExperimentApiService | `Run / Monitor` tab | Run / Monitor | tested |
| API Endpoints | `POST /experiments` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `POST /experiments/{id}/start` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `POST /experiments/{id}/stop` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments/{id}` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments/{id}/status` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments/{id}/metrics` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments/{id}/decisions` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /experiments/{id}/report` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `POST /experiments/{id}/rerun` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /scenarios` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /strategies` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| API Endpoints | `GET /compare` | FastAPI app + ExperimentApiService | `tests/test_api_fastapi.py` | tests/test_api_fastapi.py | tested |
| CLI Commands | `autorl validate-config --config ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl run --config ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl list` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl report --experiment-id ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl rerun --experiment-id ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl validate-suite` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl benchmark-elec2` | CLI + BenchmarkReplayRunner/Phase10ExperimentalSeriesRunner | CLI smoke with bounded sample replay | CLI smoke with bounded sample replay | tested |
| CLI Commands | `autorl benchmark-suite` | CLI + BenchmarkReplayRunner/Phase10ExperimentalSeriesRunner | CLI smoke with bounded suite replay | CLI smoke with bounded suite replay | tested |
| CLI Commands | `autorl run-suite --config ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl status --experiment-id ...` | CLI + ExperimentOrchestrator | CLI smoke | CLI smoke | tested |
| CLI Commands | `autorl export --experiment-id ... --format zip` | CLI + ExperimentOrchestrator | CLI smoke/export tests | CLI smoke/export tests | tested |
| Storage Elements | SQLite `experiments` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `configs` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `episode_metrics` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `window_metrics` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `decisions` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `artifacts` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | SQLite `events` | SQLiteRepository | storage tests | storage tests | tested |
| Storage Elements | Artifact `config.yaml` | ExperimentArtifactStore + reporting/export layer | storage tests | storage tests | tested |
| Storage Elements | Artifact `config_hash.txt` | ExperimentArtifactStore + reporting/export layer | storage tests | storage tests | tested |
| Storage Elements | Artifact `versions.json` | ExperimentArtifactStore + reporting/export layer | storage tests | storage tests | tested |
| Storage Elements | Artifact `metrics.csv` | ExperimentArtifactStore + reporting/export layer | storage/report tests | storage/report tests | tested |
| Storage Elements | Artifact `window_metrics.csv` | ExperimentArtifactStore + reporting/export layer | storage/report tests | storage/report tests | tested |
| Storage Elements | Artifact `decisions.csv` | ExperimentArtifactStore + reporting/export layer | storage/report tests | storage/report tests | tested |
| Storage Elements | Artifact `events.log` | ExperimentArtifactStore + reporting/export layer | storage tests | storage tests | tested |
| Storage Elements | Artifact `report.md` | ExperimentArtifactStore + reporting/export layer | report tests | report tests | tested |
| Storage Elements | Artifact `reward_curve.png` | ExperimentArtifactStore + reporting/export layer | report tests | report tests | tested |
| Storage Elements | Artifact `strategy_timeline.png` | ExperimentArtifactStore + reporting/export layer | report tests | report tests | tested |
| Storage Elements | Artifact `utility_lcb.png` | ExperimentArtifactStore + reporting/export layer | report tests | report tests | tested |
| System and Experimental Validation Items | SE-01 | Validation suite + benchmark replay + UI workflow checks | stationary e2e + LCB no-switch replay test | stationary e2e + LCB no-switch replay test | tested |
| System and Experimental Validation Items | SE-02 | Validation suite + benchmark replay + UI workflow checks | validation suite | validation suite | tested |
| System and Experimental Validation Items | SE-03 | Validation suite + benchmark replay + UI workflow checks | validation suite | validation suite | tested |
| System and Experimental Validation Items | SE-04 | Validation suite + benchmark replay + UI workflow checks | LCB vs recent-leader false-switch replay test | LCB vs recent-leader false-switch replay test | tested |
| System and Experimental Validation Items | SE-05 | Validation suite + benchmark replay + UI workflow checks | fallback tests | fallback tests | tested |
| System and Experimental Validation Items | SE-06 | Validation suite + benchmark replay + UI workflow checks | rerun/reproducibility tests | rerun/reproducibility tests | tested |
| System and Experimental Validation Items | SE-07 | Validation suite + benchmark replay + UI workflow checks | `tests/test_ui_streamlit.py` | tests/test_ui_streamlit.py | tested |
| System and Experimental Validation Items | EXP-01 | Validation suite + benchmark replay + UI workflow checks | benchmark profile suite runner + comparator suite smoke | benchmark profile suite runner + comparator suite smoke | tested |
| System and Experimental Validation Items | EXP-02 | Validation suite + benchmark replay + UI workflow checks | `h1_drift_aware_v2` profile runner smoke | h1_drift_aware_v2 | tested |
| System and Experimental Validation Items | EXP-03 | Validation suite + benchmark replay + UI workflow checks | `h2_search` profile runner smoke | h2_search | tested |
| System and Experimental Validation Items | EXP-04 | Validation suite + benchmark replay + UI workflow checks | `h2_tempered_*` profile runner smoke | h2_tempered_* | tested |
| System and Experimental Validation Items | EXP-05 | Validation suite + benchmark replay + UI workflow checks | explicit comparator profiles + benchmark suite smoke | explicit comparator profiles + benchmark suite smoke | tested |
| Documentation Deliverables | DOC-01 | Documentation package in docs/ + README | `docs/doc_01_use_case_diagram.md` | docs/doc_01_use_case_diagram.md | tested |
| Documentation Deliverables | DOC-02 | Documentation package in docs/ + README | `docs/doc_02_dfd_level_0.md` | docs/doc_02_dfd_level_0.md | tested |
| Documentation Deliverables | DOC-03 | Documentation package in docs/ + README | `docs/doc_03_component_diagram.md` | docs/doc_03_component_diagram.md | tested |
| Documentation Deliverables | DOC-04 | Documentation package in docs/ + README | `docs/doc_04_sequence_stay_switch.md` | docs/doc_04_sequence_stay_switch.md | tested |
| Documentation Deliverables | DOC-05 | Documentation package in docs/ + README | `docs/doc_05_state_machine.md` | docs/doc_05_state_machine.md | tested |
| Documentation Deliverables | DOC-06 | Documentation package in docs/ + README | `docs/doc_06_er_schema.md` | docs/doc_06_er_schema.md | tested |
| Documentation Deliverables | DOC-07 | Documentation package in docs/ + README | `docs/doc_07_deployment_diagram.md` | docs/doc_07_deployment_diagram.md | tested |
| Documentation Deliverables | DOC-08 | Documentation package in docs/ + README | `docs/requirements_traceability.md` | docs/requirements_traceability.md | tested |
| Documentation Deliverables | DOC-09 | Documentation package in docs/ + README | `docs/doc_09_moscow_requirements.md` | docs/doc_09_moscow_requirements.md | tested |
| Documentation Deliverables | DOC-10 | Documentation package in docs/ + README | `docs/doc_10_operational_instruction.md`, `docs/operations_manual.md` | docs/doc_10_operational_instruction.md; docs/operations_manual.md | tested |

## Notes

- `Artifact Result` records the concrete file, test, or artifact path already referenced by the requirements inventory.
- Benchmark replay items use deterministic temporal replay where the artifact summaries explicitly document `seed_protocol`, `n`, uncertainty intervals, and interpretation limits.
- Documentation items `DOC-01..DOC-10` are represented by their Markdown/Mermaid equivalents in `docs/`.

