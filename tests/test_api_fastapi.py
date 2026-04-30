"""FastAPI backend tests for phase 8."""

from __future__ import annotations

import time
from pathlib import Path

from fastapi.testclient import TestClient

from autorl.interfaces.api import create_app


def _api_config(tmp_path: Path, *, name: str, mode: str = "adaptive") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "experiment_name": name,
        "seed": 42,
        "mode": mode,
        "scenario": {
            "name": "stationary",
            "episodes": 24,
            "steps_per_episode": 8,
            "tags": ["api", "phase8"],
            "description": "API-backed stationary scenario.",
        },
        "strategies": [
            {
                "name": "fixed",
                "parameters": {"fixed_action_index": 0},
                "compute_cost": 0.05,
            },
            {
                "name": "adaptive_meta",
                "parameters": {"temperature": 0.6},
                "compute_cost": 0.20,
            },
        ],
        "meta_controller": {
            "window_size": 6,
            "min_samples": 3,
            "delta": 0.01,
            "lambda": 0.0,
            "switch_cost": 0.05,
            "utility_weights": {
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        },
        "artifacts_root": str(tmp_path / "artifacts"),
        "tags": ["api", "phase8"],
        "notes": "FastAPI lifecycle test config.",
    }


def _wait_for_terminal_status(client: TestClient, experiment_id: str, timeout_s: float = 15.0) -> dict[str, object]:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        response = client.get(f"/experiments/{experiment_id}/status")
        payload = response.json()
        if payload["status"] in {"completed", "failed", "stopped"}:
            return payload
        time.sleep(0.05)
    raise AssertionError(f"experiment {experiment_id} did not finish within {timeout_s} seconds")


def test_fastapi_full_experiment_lifecycle(tmp_path: Path) -> None:
    app = create_app(artifacts_root=tmp_path / "artifacts")
    client = TestClient(app)

    assert client.get("/health").json()["status"] == "ok"
    assert any(item["name"] == "stationary" for item in client.get("/scenarios").json())
    assert any(item["name"] == "adaptive_meta" for item in client.get("/strategies").json())

    create_response = client.post("/experiments", json=_api_config(tmp_path, name="api-adaptive"))
    assert create_response.status_code == 201
    experiment_id = create_response.json()["experiment_id"]

    details_response = client.get(f"/experiments/{experiment_id}")
    assert details_response.status_code == 200
    assert details_response.json()["experiment"]["status"] == "created"

    start_response = client.post(f"/experiments/{experiment_id}/start")
    assert start_response.status_code == 202
    assert start_response.json()["status"] == "running"

    terminal_status = _wait_for_terminal_status(client, experiment_id)
    assert terminal_status["status"] == "completed"
    assert terminal_status["episode_count"] == 24

    metrics_response = client.get(f"/experiments/{experiment_id}/metrics")
    assert metrics_response.status_code == 200
    metrics_payload = metrics_response.json()
    assert len(metrics_payload["episode_metrics"]) == 24
    assert metrics_payload["window_metrics"]

    decisions_response = client.get(f"/experiments/{experiment_id}/decisions")
    assert decisions_response.status_code == 200
    assert isinstance(decisions_response.json(), list)

    report_response = client.get(f"/experiments/{experiment_id}/report")
    assert report_response.status_code == 200
    assert "# AutoRL Experiment Report" in report_response.json()["report_markdown"]

    list_response = client.get("/experiments")
    assert list_response.status_code == 200
    assert any(row["experiment_id"] == experiment_id for row in list_response.json())

    rerun_response = client.post(f"/experiments/{experiment_id}/rerun")
    assert rerun_response.status_code == 202
    rerun_experiment_id = rerun_response.json()["experiment_id"]
    rerun_status = _wait_for_terminal_status(client, rerun_experiment_id)
    assert rerun_status["status"] == "completed"

    compare_response = client.get("/compare", params=[("experiment_ids", experiment_id), ("experiment_ids", rerun_experiment_id)])
    assert compare_response.status_code == 200
    comparison_rows = compare_response.json()
    assert {row["experiment_id"] for row in comparison_rows} == {experiment_id, rerun_experiment_id}


def test_fastapi_stop_and_error_paths(tmp_path: Path) -> None:
    app = create_app(artifacts_root=tmp_path / "artifacts")
    client = TestClient(app)

    invalid_response = client.post("/experiments", json={"experiment_name": ""})
    assert invalid_response.status_code == 422

    create_response = client.post("/experiments", json=_api_config(tmp_path, name="api-stop"))
    experiment_id = create_response.json()["experiment_id"]

    stop_response = client.post(f"/experiments/{experiment_id}/stop")
    assert stop_response.status_code == 202
    assert stop_response.json()["status"] == "created"

    missing_response = client.get("/experiments/missing-id/status")
    assert missing_response.status_code == 404
