"""FastAPI application factory for phase 8."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, Query, status

from autorl.application.api_service import ExperimentApiService
from autorl.domain.errors import ConfigValidationError


def create_app(*, artifacts_root: str | Path = "artifacts") -> FastAPI:
    """Create the FastAPI application."""
    service = ExperimentApiService(default_artifacts_root=artifacts_root)
    app = FastAPI(title="AutoRL Strategy Manager API", version="0.1.0")
    app.state.api_service = service

    def get_service() -> ExperimentApiService:
        return app.state.api_service

    @app.get("/health")
    def health(api_service=Depends(get_service)) -> dict[str, object]:
        return api_service.health()

    @app.get("/scenarios")
    def list_scenarios(api_service=Depends(get_service)) -> list[dict[str, str]]:
        return api_service.list_scenarios()

    @app.get("/strategies")
    def list_strategies(api_service=Depends(get_service)) -> list[dict[str, str]]:
        return api_service.list_strategies()

    @app.post("/experiments", status_code=status.HTTP_201_CREATED)
    def create_experiment(
        payload: dict[str, Any],
        api_service=Depends(get_service),
    ) -> dict[str, str]:
        created = api_service.create_experiment(payload)
        return {
            "experiment_id": created.experiment_id,
            "status": created.status,
            "artifacts_path": created.artifacts_path,
            "config_hash": created.config_hash,
        }

    @app.post("/experiments/{experiment_id}/start", status_code=status.HTTP_202_ACCEPTED)
    def start_experiment(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, Any]:
        return api_service.start_experiment(experiment_id)

    @app.post("/experiments/{experiment_id}/stop", status_code=status.HTTP_202_ACCEPTED)
    def stop_experiment(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, Any]:
        return api_service.stop_experiment(experiment_id)

    @app.get("/experiments")
    def list_experiments(api_service=Depends(get_service)) -> list[dict[str, Any]]:
        return api_service.list_experiments()

    @app.get("/experiments/{experiment_id}")
    def get_experiment(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, Any]:
        return api_service.get_experiment(experiment_id)

    @app.get("/experiments/{experiment_id}/status")
    def get_experiment_status(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, Any]:
        return api_service.get_status(experiment_id)

    @app.get("/experiments/{experiment_id}/metrics")
    def get_metrics(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, list[dict[str, Any]]]:
        return api_service.get_metrics(experiment_id)

    @app.get("/experiments/{experiment_id}/decisions")
    def get_decisions(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> list[dict[str, Any]]:
        return api_service.get_decisions(experiment_id)

    @app.get("/experiments/{experiment_id}/report")
    def get_report(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, str]:
        return api_service.get_report(experiment_id)

    @app.post("/experiments/{experiment_id}/rerun", status_code=status.HTTP_202_ACCEPTED)
    def rerun_experiment(
        experiment_id: str,
        api_service=Depends(get_service),
    ) -> dict[str, Any]:
        return api_service.rerun_experiment(experiment_id)

    @app.get("/compare")
    def compare_experiments(
        experiment_ids: list[str] | None = Query(default=None),
        api_service=Depends(get_service),
    ) -> list[dict[str, Any]]:
        return api_service.compare_experiments(experiment_ids)

    @app.exception_handler(FileNotFoundError)
    async def not_found_handler(_, exc: FileNotFoundError):
        return _json_error(status.HTTP_404_NOT_FOUND, str(exc))

    @app.exception_handler(ConfigValidationError)
    async def config_error_handler(_, exc: ConfigValidationError):
        return _json_error(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc))

    return app


def _json_error(status_code: int, detail: str):
    """Build a small JSON error response."""
    from fastapi.responses import JSONResponse

    return JSONResponse(status_code=status_code, content={"detail": detail})
