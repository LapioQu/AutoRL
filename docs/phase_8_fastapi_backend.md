# Phase 8 FastAPI Backend

Phase 8 adds the first programmatic backend for the local AutoRL system.
This document is phase-scoped; final closure status across later work is tracked in [requirements_inventory.md](/E:/dipproj/docs/requirements_inventory.md).

## Implemented Scope

- FastAPI application factory in `src/autorl/interfaces/api/app.py`
- API-facing application service in `src/autorl/application/api_service.py`
- artifact-backed experiment draft creation before execution
- background `start` execution through shared application services
- cooperative `stop` request flag for API-triggered runs
- endpoints:
  - `GET /health`
  - `GET /scenarios`
  - `GET /strategies`
  - `POST /experiments`
  - `POST /experiments/{id}/start`
  - `POST /experiments/{id}/stop`
  - `GET /experiments`
  - `GET /experiments/{id}`
  - `GET /experiments/{id}/status`
  - `GET /experiments/{id}/metrics`
  - `GET /experiments/{id}/decisions`
  - `GET /experiments/{id}/report`
  - `POST /experiments/{id}/rerun`
  - `GET /compare`

## Architectural Notes

- FastAPI handlers do not contain domain logic.
- API handlers call `ExperimentApiService`, which delegates to `ExperimentOrchestrator` and repository-backed readers.
- CLI and API now share the same application services, preserving metric and decision semantics.

## Verification

Primary API verification:

- `tests/test_api_fastapi.py`

Covered behavior:

- health and catalog endpoints
- experiment creation
- background start and terminal completion polling
- status endpoint
- metrics and decision retrieval
- markdown report retrieval
- rerun endpoint
- compare endpoint
- stop endpoint on a created draft
- 404 and config-validation error paths

## Current Limits

- API stop is cooperative and best-effort; the run is not yet a fully interactive online monitoring loop.
- Explicit formal orchestrator state-machine coverage is still partial.
- UI integration remains phase 9.
