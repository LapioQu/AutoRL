"""Streamlit UI tests for phase 9."""

from __future__ import annotations

import time
from pathlib import Path

from streamlit.testing.v1 import AppTest

from autorl.application import DatasetLabJobService, ExperimentApiService

APP_RUN_TIMEOUT_S = 20


def _config_payload(
    tmp_path: Path,
    *,
    name: str,
    mode: str,
    strategy_names: list[str],
) -> dict[str, object]:
    compute_costs = {
        "fixed": 0.05,
        "greedy_reward": 0.08,
        "drift_aware": 0.12,
        "lcb_conservative": 0.11,
        "tempered_reward": 0.14,
        "adaptive_meta": 0.20,
    }
    strategies = []
    for strategy_name in strategy_names:
        parameters: dict[str, object] = {}
        if strategy_name == "fixed":
            parameters["fixed_action_index"] = 0
        if strategy_name in {"tempered_reward", "adaptive_meta"}:
            parameters["temperature"] = 0.6
        strategies.append(
            {
                "name": strategy_name,
                "parameters": parameters,
                "compute_cost": compute_costs[strategy_name],
            }
        )
    return {
        "schema_version": "1.0",
        "experiment_name": name,
        "seed": 42,
        "mode": mode,
        "scenario": {
            "name": "stationary",
            "episodes": 24,
            "steps_per_episode": 8,
            "tags": ["ui", "phase9"],
            "description": "UI-backed stationary scenario.",
        },
        "strategies": strategies,
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
        "tags": ["ui", "phase9"],
        "notes": "Streamlit smoke test config.",
    }


def _wait_for_completed(service: ExperimentApiService, experiment_id: str, artifacts_root: Path, timeout_s: float = 15.0) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        status = service.get_status(experiment_id, artifacts_root=artifacts_root)
        if status["status"] in {"completed", "failed", "stopped"}:
            assert status["status"] == "completed"
            return
        time.sleep(0.05)
    raise AssertionError(f"experiment {experiment_id} did not finish within {timeout_s} seconds")


def _find_widget(widgets, label: str):
    for widget in widgets:
        if getattr(widget, "label", None) == label:
            return widget
    raise AssertionError(f"widget with label {label!r} not found")


def test_streamlit_ui_reads_real_artifacts_and_runs_workflow(tmp_path: Path, monkeypatch) -> None:
    artifacts_root = tmp_path / "artifacts"
    monkeypatch.setenv("AUTORL_UI_ARTIFACTS_ROOT", str(artifacts_root))

    service = ExperimentApiService(default_artifacts_root=artifacts_root)
    dataset_job_service = DatasetLabJobService(default_artifacts_root=artifacts_root)
    baseline = service.create_experiment(
        _config_payload(
            tmp_path,
            name="ui-baseline",
            mode="baseline",
            strategy_names=["fixed"],
        )
    )
    service.start_experiment(baseline.experiment_id, artifacts_root=artifacts_root)
    _wait_for_completed(service, baseline.experiment_id, artifacts_root)

    comparison = service.create_experiment(
        _config_payload(
            tmp_path,
            name="ui-comparison",
            mode="adaptive",
            strategy_names=["fixed", "adaptive_meta"],
        )
    )
    service.start_experiment(comparison.experiment_id, artifacts_root=artifacts_root)
    _wait_for_completed(service, comparison.experiment_id, artifacts_root)

    pending = service.create_experiment(
        _config_payload(
            tmp_path,
            name="ui-pending",
            mode="adaptive",
            strategy_names=["fixed", "adaptive_meta"],
        )
    )

    app = AppTest.from_file("src/autorl/interfaces/ui/app.py").run(timeout=APP_RUN_TIMEOUT_S)
    assert app.title[0].value == "AutoRL Strategy Manager"
    assert set(_find_widget(app.radio, "Режим").options) == {"Студія прогнозування", "Моніторинг виконання", "Звіти та докази"}

    _find_widget(app.radio, "Режим").set_value("Моніторинг виконання")
    app.run(timeout=APP_RUN_TIMEOUT_S)
    selected_widget = _find_widget(app.selectbox, "Запуск для перегляду")
    selected_widget.select(pending.experiment_id)
    app.run(timeout=APP_RUN_TIMEOUT_S)

    _find_widget(app.button, "Запустити вибраний експеримент").click()
    app.run(timeout=APP_RUN_TIMEOUT_S)

    deadline = time.time() + 15.0
    while time.time() < deadline:
        app.run(timeout=APP_RUN_TIMEOUT_S)
        status_value = _find_widget(app.metric, "Статус").value
        if status_value in {"completed", "failed", "stopped"}:
            assert status_value == "completed"
            break
        time.sleep(0.05)
    else:
        raise AssertionError("UI-driven experiment did not complete in time")

    assert any("Поточна динаміка винагороди" in item.value for item in app.markdown)
    assert any("Стан запусків" in item.value for item in app.subheader)

    _find_widget(app.radio, "Режим").set_value("Звіти та докази")
    app.run(timeout=APP_RUN_TIMEOUT_S)
    assert any("Порівняння стратегій і запусків" in item.value for item in app.subheader)
    compare_widget = _find_widget(app.multiselect, "Експерименти для порівняння")
    compare_widget.set_value([baseline.experiment_id, comparison.experiment_id, pending.experiment_id])
    app.run(timeout=APP_RUN_TIMEOUT_S)
    comparison_frames = [frame.value for frame in app.dataframe if "reward_mean" in frame.value.columns and "experiment_id" in frame.value.columns]
    assert comparison_frames
    assert set(comparison_frames[-1]["experiment_id"]) == {baseline.experiment_id, comparison.experiment_id, pending.experiment_id}
    assert any("AutoRL Experiment Report" in item.value for item in app.markdown)

    export_frames = [frame.value for frame in app.dataframe if "kind" in frame.value.columns and "path" in frame.value.columns]
    assert export_frames
    artifact_names = set(Path(path).name for path in export_frames[-1]["path"])
    assert {"report.md", "metrics.csv", "decisions.csv"} <= artifact_names

    _find_widget(app.radio, "Режим").set_value("Студія прогнозування")
    app.run(timeout=APP_RUN_TIMEOUT_S)
    assert set(_find_widget(app.radio, "Джерело датасету").options) == {"Готовий датасет", "Завантажити CSV", "Вставити CSV"}
    _find_widget(app.radio, "Джерело датасету").set_value("Вставити CSV")
    app.run(timeout=APP_RUN_TIMEOUT_S)
    _find_widget(
        app.text_area,
        "Вставте CSV-дані",
    ).set_value(
        "\n".join(
            [
                "timestamp,signal,target",
                "1,0.1,10",
                "2,0.2,11",
                "3,0.4,13",
                "4,0.7,16",
                "5,1.0,20",
                "6,1.1,25",
                "7,1.4,31",
                "8,1.9,38",
                "9,2.1,46",
                "10,2.4,55",
            ]
        )
    )
    app.run(timeout=APP_RUN_TIMEOUT_S)
    _find_widget(app.text_area, "Опишіть рядки для додавання").set_value("timestamp=11, signal=2.8, target=")
    _find_widget(app.button, "Інтерпретувати рядки").click()
    app.run(timeout=APP_RUN_TIMEOUT_S)
    _find_widget(app.button, "Аналізувати датасет і побудувати прогноз").click()
    app.run(timeout=APP_RUN_TIMEOUT_S)
    jobs = dataset_job_service.list_jobs(artifacts_root=artifacts_root)
    assert jobs
    dataset_job_id = jobs[0].job_id
    deadline = time.time() + 10.0
    while time.time() < deadline:
        status = dataset_job_service.get_job_status(dataset_job_id, artifacts_root=artifacts_root)
        if status.status in {"completed", "failed"}:
            assert status.status == "completed"
            break
        time.sleep(0.05)
    else:
        raise AssertionError("dataset-lab job did not complete in time")

    monitor_app = AppTest.from_file("src/autorl/interfaces/ui/app.py").run(timeout=APP_RUN_TIMEOUT_S)
    _find_widget(monitor_app.radio, "Режим").set_value("Моніторинг виконання")
    monitor_app.run(timeout=APP_RUN_TIMEOUT_S)
    assert any("Фонові аналізи датасетів" in item.value for item in monitor_app.subheader)
    assert any("Запуск аналізу для перегляду" == widget.label for widget in monitor_app.selectbox)

    evidence_app = AppTest.from_file("src/autorl/interfaces/ui/app.py").run(timeout=APP_RUN_TIMEOUT_S)
    _find_widget(evidence_app.radio, "Режим").set_value("Звіти та докази")
    evidence_app.run(timeout=APP_RUN_TIMEOUT_S)
    assert any("Звіти аналізів датасетів" in item.value for item in evidence_app.subheader)
    assert any("Результат перевірки" in item.value for item in evidence_app.markdown)
