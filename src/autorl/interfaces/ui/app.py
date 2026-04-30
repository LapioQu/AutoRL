"""Streamlit UI for phase 9."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import html
import json
import os
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any
from urllib.parse import parse_qs, urlparse

import streamlit as st
import streamlit.components.v1 as components

from autorl.application import (
    DatasetLabJobService,
    DatasetLabJobStatus,
    DatasetLabResult,
    DatasetLabService,
    ExperimentApiService,
)


DEFAULT_STRATEGIES = [
    "fixed",
    "greedy_reward",
    "drift_aware",
    "lcb_conservative",
    "tempered_reward",
    "adaptive_meta",
]


@st.cache_resource(show_spinner=False)
def get_service(artifacts_root: str) -> ExperimentApiService:
    """Build one shared UI service per artifacts root."""
    return ExperimentApiService(default_artifacts_root=artifacts_root)


@st.cache_resource(show_spinner=False)
def get_dataset_lab_service(artifacts_root: str) -> DatasetLabService:
    """Build one shared dataset-lab service per artifacts root."""
    return DatasetLabService(default_artifacts_root=artifacts_root)


@st.cache_resource(show_spinner=False)
def get_dataset_lab_job_service(artifacts_root: str) -> DatasetLabJobService:
    """Build one shared dataset-lab job service per artifacts root."""
    return DatasetLabJobService(default_artifacts_root=artifacts_root)


@st.cache_resource(show_spinner=False)
def get_live_monitor_base_url() -> str:
    """Start one lightweight local JSON server for flicker-free monitor panels."""

    class _LiveMonitorHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

        def _send_json(self, payload: Any, *, status_code: int = 200) -> bool:
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            try:
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(encoded)
                return True
            except OSError:
                return False

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            artifacts_root = query.get("artifacts_root", ["artifacts"])[0]
            job_id = query.get("job_id", [""])[0]
            limit = int(query.get("limit", ["240"])[0])
            service = DatasetLabJobService(default_artifacts_root=artifacts_root)

            try:
                if parsed.path == "/dataset-lab/job-status":
                    status = service.get_job_status(job_id, artifacts_root=artifacts_root)
                    self._send_json(asdict(status))
                    return
                if parsed.path == "/dataset-lab/telemetry":
                    telemetry = service.load_telemetry(job_id, artifacts_root=artifacts_root, limit=limit)
                    self._send_json(telemetry)
                    return
                if parsed.path == "/dataset-lab/jobs":
                    jobs = service.list_jobs(artifacts_root=artifacts_root, limit=limit)
                    self._send_json([asdict(job) for job in jobs])
                    return
            except FileNotFoundError as exc:
                self._send_json({"detail": str(exc)}, status_code=404)
                return
            except OSError:
                return
            except Exception as exc:  # pragma: no cover - defensive live server path
                self._send_json({"detail": str(exc)}, status_code=500)
                return

            self._send_json({"detail": "not found"}, status_code=404)

    server = ThreadingHTTPServer(("127.0.0.1", 0), _LiveMonitorHandler)
    thread = Thread(target=server.serve_forever, daemon=True, name="autorl-ui-live-monitor")
    thread.start()
    return f"http://127.0.0.1:{server.server_port}"


def main() -> None:
    """Run the Streamlit UI."""
    st.set_page_config(
        page_title="AutoRL Strategy Manager",
        page_icon="A",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _apply_theme()
    _ensure_ui_state_defaults()
    pending_view = st.session_state.pop("pending_ui_view", None)
    if pending_view is not None:
        st.session_state["ui_view"] = pending_view

    st.title("AutoRL Strategy Manager")
    st.caption("Адаптивне перемикання стратегій, моніторинг виконання, прогнозування на датасетах і зрозуміла інтерпретація рішень.")
    _render_flash_notice()

    artifacts_root = _render_sidebar()
    service = get_service(artifacts_root)
    dataset_lab_service = get_dataset_lab_service(artifacts_root)
    dataset_lab_job_service = get_dataset_lab_job_service(artifacts_root)
    experiments = service.list_experiments(artifacts_root=artifacts_root)
    selected_experiment_id = _default_selected_experiment(experiments)
    current_view = st.session_state.get("ui_view", "Студія прогнозування")

    _render_hero(experiments, current_view=current_view)

    if current_view == "Студія прогнозування":
        _render_dataset_lab(
            dataset_lab_service=dataset_lab_service,
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
        )
        return

    if current_view == "Моніторинг виконання":
        _render_operations_monitor_page(
            service=service,
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
            selected_experiment_id=selected_experiment_id,
        )
        return

    if current_view == "Звіти та докази":
        _render_evidence_page(
            service=service,
            dataset_lab_service=dataset_lab_service,
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
            experiments=experiments,
            selected_experiment_id=selected_experiment_id,
        )
        return


def _render_sidebar() -> str:
    with st.sidebar:
        st.header("Робоча область")
        view = st.radio(
            "Режим",
            options=["Студія прогнозування", "Моніторинг виконання", "Звіти та докази"],
            index=["Студія прогнозування", "Моніторинг виконання", "Звіти та докази"].index(st.session_state.get("ui_view", "Студія прогнозування")),
            key="ui_view",
        )
        if view == "Студія прогнозування":
            st.caption("Завантажте один CSV, порівняйте adaptive з best fixed і одразу отримайте прогноз наступного кроку.")
        elif view == "Моніторинг виконання":
            st.caption("Слідкуйте за реальним adaptive-запуском, його прогресом і перемиканням стратегій під час виконання.")
        else:
            st.caption("Відкривайте звіти, порівнюйте попередні запуски і експортуйте докази для рішень.")
        st.divider()
        artifacts_root = st.text_input(
            "Каталог артефактів",
            value=st.session_state.get("artifacts_root", os.environ.get("AUTORL_UI_ARTIFACTS_ROOT", "artifacts")),
            key="artifacts_root",
        )
        st.caption("Усі аналізи завантажених датасетів і збережені звіти читаються з цього каталогу.")
    return artifacts_root


def _ensure_ui_state_defaults() -> None:
    defaults = {
        "dataset_lab_source_mode": "Готовий датасет",
        "dataset_lab_csv_text": "",
        "dataset_lab_name": "pasted-stream",
        "dataset_lab_manual_text": "",
        "dataset_lab_target": "",
        "dataset_lab_order": "<use current row order>",
        "dataset_lab_task_type": "auto",
        "dataset_lab_policy_name": "auto_meta",
        "dataset_lab_lag_count": 3,
        "dataset_lab_use_manual_limit": False,
        "dataset_lab_max_rows": 0,
        "dataset_lab_builtin_rows": 0,
        "selected_dataset_job_id": "",
        "live_auto_refresh": True,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _apply_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
            color: #0f172a;
        }
        html, body, .stApp, .stApp * {
            animation: none !important;
            transition: none !important;
        }
        [data-testid="stSkeleton"] {
            display: none !important;
        }
        .stApp, .stApp [data-testid="stMarkdownContainer"] p, .stApp label, .stApp div {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            color: #0f172a;
        }
        h1, h2, h3, .stTabs [data-baseweb="tab"] {
            font-family: "Segoe UI Semibold", "Segoe UI", Tahoma, sans-serif;
            letter-spacing: 0.01em;
            color: #0f172a;
        }
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] span {
            color: #334155;
            font-size: 1rem;
            line-height: 1.55;
        }
        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #dbe3ee;
            border-radius: 20px;
            padding: 1rem 1rem 0.8rem 1rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #163247 0%, #23465f 100%);
        }
        [data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.45rem;
        }
        .stTabs [data-baseweb="tab"] {
            background: #dbe3ee;
            border-radius: 999px;
            padding: 0.55rem 1rem;
            color: #163247 !important;
        }
        .stTabs [aria-selected="true"] {
            background: #163247 !important;
            color: #f8fafc !important;
        }
        .stTabs [aria-selected="true"] * {
            color: #f8fafc !important;
        }
        .stButton > button,
        .stDownloadButton > button,
        [data-baseweb="button"],
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondary"] {
            background: #163247;
            color: #f8fafc !important;
            border: 1px solid #163247;
        }
        .stButton > button *,
        .stDownloadButton > button *,
        [data-baseweb="button"] *,
        [data-testid="stBaseButton-primary"] *,
        [data-testid="stBaseButton-secondary"] * {
            color: #f8fafc !important;
            fill: #f8fafc !important;
        }
        .stButton > button[kind="primary"] {
            background: #163247;
            color: #f8fafc;
            border: 1px solid #163247;
        }
        .stButton > button[kind="primary"] * {
            color: #f8fafc !important;
            fill: #f8fafc !important;
        }
        [data-testid="stSelectbox"] div[data-baseweb="select"],
        [data-testid="stSelectbox"] div[data-baseweb="select"] *,
        [data-testid="stMultiSelect"] div[data-baseweb="select"],
        [data-testid="stMultiSelect"] div[data-baseweb="select"] *,
        div[data-baseweb="select"],
        div[data-baseweb="select"] *,
        div[data-baseweb="popover"] *,
        div[role="option"],
        div[role="option"] *,
        li[role="option"],
        li[role="option"] *,
        div[role="listbox"],
        div[role="listbox"] *,
        ul[role="listbox"],
        ul[role="listbox"] * {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            fill: #f8fafc !important;
        }
        div[data-baseweb="select"] > div {
            background: #163247 !important;
            border-color: #163247 !important;
        }
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
            background: #163247 !important;
            border-color: #163247 !important;
        }
        div[data-baseweb="select"] input::placeholder {
            color: #dbeafe !important;
            -webkit-text-fill-color: #dbeafe !important;
            opacity: 1 !important;
        }
        div[data-baseweb="popover"],
        div[role="listbox"],
        ul[role="listbox"] {
            background: #163247 !important;
        }
        [data-testid="stSelectbox"] svg,
        [data-testid="stMultiSelect"] svg,
        div[data-baseweb="select"] svg {
            color: #f8fafc !important;
            fill: #f8fafc !important;
            stroke: #f8fafc !important;
        }
        div[role="option"],
        li[role="option"] {
            background: #163247 !important;
            color: #f8fafc !important;
        }
        div[role="option"][aria-selected="true"],
        li[role="option"][aria-selected="true"] {
            background: #28516d !important;
            color: #f8fafc !important;
        }
        .stExpander {
            background: #ffffff;
            border: 1px solid #dbe3ee;
            border-radius: 18px;
        }
        .hero-card {
            border-radius: 24px;
            padding: 1.2rem 1.35rem;
            background: #ffffff;
            border: 1px solid #dbe3ee;
            box-shadow: 0 18px 36px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        }
        .section-card {
            border-radius: 22px;
            padding: 1.2rem 1.25rem;
            background: #ffffff;
            border: 1px solid #dbe3ee;
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.04);
            margin-bottom: 1rem;
        }
        .insight-card {
            border-left: 5px solid #0f766e;
            background: #f8fffc;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
        }
        .warning-card {
            border-left: 5px solid #b45309;
            background: #fff8f0;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.8rem;
        }
        .metric-strip {
            border-radius: 18px;
            padding: 0.9rem 1rem;
            background: #f8fafc;
            border: 1px solid #dbe3ee;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero(experiments: list[dict[str, Any]], *, current_view: str) -> None:
    latest_status = experiments[0]["status"] if experiments else "ще немає запусків"
    if current_view == "Студія прогнозування":
        title = "Студія прогнозування"
        body = (
            "Завантажте часовий CSV, перевірте adaptive проти best fixed та oracle і отримайте прогноз наступного кроку "
            "без переходу на іншу сторінку."
        )
    elif current_view == "Моніторинг виконання":
        title = "Моніторинг виконання"
        body = (
            "Слідкуйте за реальним adaptive-запуском, динамікою якості та змінами стратегій, поки він виконується."
        )
    else:
        title = "Звіти та докази"
        body = (
            "Порівнюйте попередні запуски, відкривайте артефакти аудиту й експортуйте докази для обґрунтування прогнозу "
            "або перемикання стратегії."
        )
    st.markdown(
        f"""
        <div class="hero-card">
            <h3 style="margin:0 0 0.35rem 0;">{title}</h3>
            <p style="margin:0;">
                {body}
                Поточний стан репозиторію: <strong>{len(experiments)}</strong> збережених експериментів,
                останній статус <strong>{latest_status}</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _default_selected_experiment(experiments: list[dict[str, Any]]) -> str | None:
    if not experiments:
        st.session_state["selected_experiment_id"] = None
        return None

    options = [row["experiment_id"] for row in experiments]
    pending = st.session_state.pop("pending_selected_experiment_id", None)
    current = st.session_state.get("selected_experiment_id")
    if pending in options:
        current = pending
    if current not in options:
        current = options[0]
    st.session_state["selected_experiment_id"] = current
    return current


def _resolve_selected_experiment(experiments: list[dict[str, Any]]) -> str | None:
    if not experiments:
        st.info("У вибраному каталозі артефактів не знайдено збережених експериментів.")
        st.session_state["selected_experiment_id"] = None
        return None

    options = [row["experiment_id"] for row in experiments]
    pending = st.session_state.pop("pending_selected_experiment_id", None)
    current = st.session_state.get("selected_experiment_id")
    if pending in options:
        current = pending
        st.session_state["selected_experiment_id"] = current
    if current not in options:
        current = options[0]
        st.session_state["selected_experiment_id"] = current

    selected = st.selectbox(
        "Вибраний експеримент",
        options=options,
        index=options.index(current),
        key="selected_experiment_selector",
    )
    st.session_state["selected_experiment_id"] = selected
    return selected


def _render_experiment_picker(experiments: list[dict[str, Any]], selected_experiment_id: str | None) -> str | None:
    if not experiments:
        st.info("У вибраному каталозі артефактів немає доступних збережених експериментів.")
        return None
    options = [row["experiment_id"] for row in experiments]
    current = selected_experiment_id if selected_experiment_id in options else options[0]
    selected = st.selectbox(
        "Запуск для перегляду",
        options=options,
        index=options.index(current),
        key="operations_selected_experiment",
    )
    st.session_state["selected_experiment_id"] = selected
    return selected


def _render_operations_monitor_page(
    *,
    service: ExperimentApiService,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    monitor_tabs = st.tabs(["Аналізи датасетів", "Експерименти"])
    with monitor_tabs[0]:
        _render_dataset_lab_monitor(
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
        )
    with monitor_tabs[1]:
        experiments = service.list_experiments(artifacts_root=artifacts_root)
        selected_experiment_id = _render_experiment_picker(experiments, selected_experiment_id)
        if selected_experiment_id is None:
            return

        top_left, top_right = st.columns([1.4, 1.0])
        with top_left:
            _render_run_monitor(
                service=service,
                artifacts_root=artifacts_root,
                selected_experiment_id=selected_experiment_id,
            )
        with top_right:
            _render_overview(
                service=service,
                artifacts_root=artifacts_root,
                experiments=experiments,
                selected_experiment_id=selected_experiment_id,
            )

        detail_tabs = st.tabs(["Продуктивність", "Хронологія", "Журнал рішень"])
        with detail_tabs[0]:
            _render_metrics_dashboard(
                service=service,
                artifacts_root=artifacts_root,
                selected_experiment_id=selected_experiment_id,
            )
        with detail_tabs[1]:
            _render_strategy_timeline(
                service=service,
                artifacts_root=artifacts_root,
                selected_experiment_id=selected_experiment_id,
            )
        with detail_tabs[2]:
            _render_decision_journal(
                service=service,
                artifacts_root=artifacts_root,
                selected_experiment_id=selected_experiment_id,
            )


def _render_evidence_page(
    *,
    service: ExperimentApiService,
    dataset_lab_service: DatasetLabService,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
    experiments: list[dict[str, Any]],
    selected_experiment_id: str | None,
) -> None:
    evidence_tabs = st.tabs(["Аналізи датасетів", "Експерименти"])
    with evidence_tabs[0]:
        _render_dataset_lab_evidence(
            dataset_lab_service=dataset_lab_service,
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
        )
    with evidence_tabs[1]:
        selected_experiment_id = _render_experiment_picker(experiments, selected_experiment_id)
        if selected_experiment_id is None:
            return

        compare_col, report_col = st.columns([1.0, 1.2])
        with compare_col:
            _render_compare(
                service=service,
                artifacts_root=artifacts_root,
                experiments=experiments,
                selected_experiment_id=selected_experiment_id,
            )
        with report_col:
            _render_reports_and_export(
                service=service,
                artifacts_root=artifacts_root,
                selected_experiment_id=selected_experiment_id,
            )


def _render_overview(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    experiments: list[dict[str, Any]],
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Стан запусків")
    total = len(experiments)
    completed = sum(1 for row in experiments if row["status"] == "completed")
    running = sum(1 for row in experiments if row["status"] == "running")
    terminal = sum(1 for row in experiments if row["status"] in {"completed", "failed", "stopped"})
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Експерименти", total)
    col2.metric("Завершено", completed)
    col3.metric("Виконується", running)
    col4.metric("У кінцевому стані", terminal)

    if selected_experiment_id is None:
        return

    details = service.get_experiment(selected_experiment_id, artifacts_root=artifacts_root)
    experiment_row = details["experiment"]
    metrics = service.get_metrics(selected_experiment_id, artifacts_root=artifacts_root)
    decisions = service.get_decisions(selected_experiment_id, artifacts_root=artifacts_root)
    st.markdown(
        f"""
        <div class="hero-card">
            <strong>{experiment_row['experiment_name']}</strong><br/>
            сценарій: <strong>{experiment_row['scenario_name']}</strong><br/>
            статус: <strong>{experiment_row['status']}</strong><br/>
            seed: <strong>{experiment_row['seed']}</strong><br/>
            хеш конфігурації: <code>{experiment_row['config_hash']}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for line in _build_experiment_insights(experiment_row, metrics["episode_metrics"], decisions):
        _render_insight_card(line)
    _render_reproducibility_block(experiment_row)
    with st.expander("Артефакти та події"):
        st.dataframe(details["artifacts"], width="stretch", hide_index=True)
        if details["events"]:
            st.dataframe(details["events"], width="stretch", hide_index=True)


def _render_create_experiment(*, service: ExperimentApiService, artifacts_root: str) -> None:
    st.subheader("Створити експеримент")
    scenario_names = [item["name"] for item in service.list_scenarios()]
    strategy_names = [item["name"] for item in service.list_strategies()]

    experiment_name = st.text_input("Назва експерименту", value="phase9-ui-run", key="create_experiment_name")
    mode = st.selectbox("Режим запуску", options=["adaptive", "baseline"], key="create_mode")
    scenario_name = st.selectbox("Сценарій", options=scenario_names, index=0, key="create_scenario")
    seed = int(st.number_input("Seed", min_value=1, value=42, step=1, key="create_seed"))
    episodes = int(st.number_input("Кількість епізодів", min_value=8, value=24, step=4, key="create_episodes"))
    steps_per_episode = int(
        st.number_input("Кроків на епізод", min_value=4, value=8, step=1, key="create_steps_per_episode")
    )
    fixed_action_index = int(
        st.selectbox("Індекс дії для fixed", options=[0, 1, 2], index=0, key="create_fixed_action_index")
    )
    primary_strategy = st.selectbox(
        "Основна стратегія для baseline-режиму",
        options=strategy_names,
        key="create_primary_strategy",
    )
    adaptive_strategies = st.multiselect(
        "Портфель стратегій для adaptive-режиму",
        options=strategy_names,
        default=DEFAULT_STRATEGIES,
        key="create_strategy_portfolio",
    )
    window_size = int(st.number_input("Розмір вікна", min_value=3, value=6, step=1, key="create_window_size"))
    min_samples = int(st.number_input("Мінімум спостережень", min_value=2, value=3, step=1, key="create_min_samples"))
    delta = float(st.number_input("Поріг delta", min_value=0.0, value=0.01, step=0.01, key="create_delta"))
    lambda_value = float(st.number_input("LCB lambda", min_value=0.0, value=0.0, step=0.1, key="create_lambda"))
    switch_cost = float(st.number_input("Вартість перемикання", min_value=0.0, value=0.05, step=0.01, key="create_switch_cost"))
    temperature = float(st.number_input("Температура", min_value=0.1, value=0.6, step=0.1, key="create_temperature"))
    notes = st.text_area("Нотатки", value="Експеримент, створений через Streamlit.", key="create_notes")

    selected_names = [primary_strategy] if mode == "baseline" else list(adaptive_strategies)
    payload = _build_config_payload(
        experiment_name=experiment_name,
        mode=mode,
        scenario_name=scenario_name,
        seed=seed,
        episodes=episodes,
        steps_per_episode=steps_per_episode,
        fixed_action_index=fixed_action_index,
        selected_strategy_names=selected_names,
        window_size=window_size,
        min_samples=min_samples,
        delta=delta,
        lambda_value=lambda_value,
        switch_cost=switch_cost,
        temperature=temperature,
        notes=notes,
        artifacts_root=artifacts_root,
    )
    st.markdown("Попередній перегляд конфігурації")
    st.json(payload, expanded=False)

    if st.button("Створити експеримент", key="create_experiment_button"):
        created = service.create_experiment(payload)
        st.session_state["selected_experiment_id"] = created.experiment_id
        st.session_state["pending_selected_experiment_id"] = created.experiment_id
        st.session_state["ui_notice"] = {
            "level": "success",
            "text": f"Експеримент {created.experiment_id} створено",
            "details": [
                f"config_hash: {created.config_hash}",
                f"artifacts_path: {created.artifacts_path}",
            ],
        }
        st.rerun()


def _render_run_monitor(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Запуск і моніторинг")
    if selected_experiment_id is None:
        st.info("Спочатку виберіть експеримент.")
        return

    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    if action_col1.button("Запустити вибраний експеримент", key="start_experiment_button"):
        response = service.start_experiment(selected_experiment_id, artifacts_root=artifacts_root)
        st.success(f"Надіслано запит на старт для {response['experiment_id']}")
    if action_col2.button("Зупинити вибраний експеримент", key="stop_experiment_button"):
        response = service.stop_experiment(selected_experiment_id, artifacts_root=artifacts_root)
        st.warning(f"Надіслано запит на зупинку, статус={response['status']}")
    if action_col3.button("Перезапустити вибраний експеримент", key="rerun_experiment_button"):
        rerun = service.rerun_experiment(selected_experiment_id, artifacts_root=artifacts_root)
        st.session_state["selected_experiment_id"] = rerun["experiment_id"]
        st.session_state["pending_selected_experiment_id"] = rerun["experiment_id"]
        st.session_state["ui_notice"] = {
            "level": "success",
            "text": f"Перезапуск створено як {rerun['experiment_id']}",
            "details": [],
        }
        st.rerun()
    action_col4.button("Оновити статус", key="refresh_status_button")

    status_payload = service.get_status(selected_experiment_id, artifacts_root=artifacts_root)
    details = service.get_experiment(selected_experiment_id, artifacts_root=artifacts_root)
    total_episodes = None
    if details["config"] is not None:
        total_episodes = details["config"]["scenario"]["episodes"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Статус", status_payload["status"])
    col2.metric("Поточний епізод", status_payload["current_episode"] if status_payload["current_episode"] is not None else "-")
    col3.metric("Перемикань", status_payload["switch_count"])
    col4.metric("Активна стратегія", status_payload["active_strategy"] or "-")

    progress_fraction = 0.0
    if total_episodes and status_payload["current_episode"] is not None:
        progress_fraction = min(1.0, float(status_payload["current_episode"] + 1) / float(total_episodes))
    elif status_payload["status"] == "completed":
        progress_fraction = 1.0
    st.progress(progress_fraction, text=_progress_text(status_payload["status"], status_payload["current_episode"], total_episodes))

    if status_payload["background_running"]:
        st.info("Фоновий запуск активний. Автооновлення тримає моніторинг близьким до реального часу, поки надходять рядки в SQLite.")
    if status_payload["error_message"]:
        st.error(status_payload["error_message"])

    metrics = service.get_metrics(selected_experiment_id, artifacts_root=artifacts_root)
    episode_metrics = metrics["episode_metrics"]
    decisions = service.get_decisions(selected_experiment_id, artifacts_root=artifacts_root)
    if episode_metrics:
        st.markdown("Поточна динаміка винагороди")
        st.line_chart(
            {
                "reward": [row["reward"] for row in episode_metrics[-24:]],
                "learning_progress": [row["learning_progress"] for row in episode_metrics[-24:]],
            }
        )
    for line in _build_experiment_insights(details["experiment"], episode_metrics, decisions):
        _render_insight_card(line)
    if details["events"]:
        st.markdown("Журнал подій")
        st.dataframe(details["events"], width="stretch", hide_index=True)
    _maybe_auto_refresh(status_payload["status"])


def _render_metrics_dashboard(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Панель метрик")
    if selected_experiment_id is None:
        st.info("Спочатку виберіть експеримент.")
        return

    metrics = service.get_metrics(selected_experiment_id, artifacts_root=artifacts_root)
    episode_metrics = metrics["episode_metrics"]
    window_metrics = metrics["window_metrics"]
    if not episode_metrics:
        st.info("Метрики епізодів ще відсутні. Спочатку запустіть експеримент.")
        return

    st.markdown("Винагорода по епізодах і прогрес навчання")
    st.line_chart(
        {
            "reward": [row["reward"] for row in episode_metrics],
            "learning_progress": [row["learning_progress"] for row in episode_metrics],
        }
    )

    if window_metrics:
        st.markdown("Середня винагорода та дисперсія по вікнах")
        st.line_chart(
            {
                "reward_mean": [row["reward_mean"] for row in window_metrics],
                "reward_variance": [row["reward_variance"] for row in window_metrics],
                "success_rate": [row["success_rate"] for row in window_metrics],
            }
        )

    details = service.get_experiment(selected_experiment_id, artifacts_root=artifacts_root)
    experiment_row = details["experiment"]
    utility_plot_path = Path(experiment_row["artifacts_path"]) / "utility_lcb.png"
    if utility_plot_path.exists():
        st.markdown("Графік utility / LCB")
        st.image(str(utility_plot_path), width="stretch")

    latest_reward = episode_metrics[-1]["reward"]
    latest_progress = episode_metrics[-1]["learning_progress"]
    st.markdown(
        f"""
        <div class="insight-card">
            <strong>Короткий аналітичний висновок.</strong> Остання зафіксована винагорода становить <strong>{latest_reward:.4f}</strong>,
            а останній прогрес навчання дорівнює <strong>{latest_progress:.4f}</strong>. Розглядайте це разом із подіями перемикання,
            щоб зрозуміти, чи контролер уже стабілізується, чи ще досліджує нові режими.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_strategy_timeline(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Хронологія стратегій")
    if selected_experiment_id is None:
        st.info("Спочатку виберіть експеримент.")
        return

    metrics = service.get_metrics(selected_experiment_id, artifacts_root=artifacts_root)
    episode_metrics = metrics["episode_metrics"]
    if not episode_metrics:
        st.info("Хронологія стратегій ще відсутня. Спочатку запустіть експеримент.")
        return

    details = service.get_experiment(selected_experiment_id, artifacts_root=artifacts_root)
    experiment_row = details["experiment"]
    timeline_plot_path = Path(experiment_row["artifacts_path"]) / "strategy_timeline.png"
    if timeline_plot_path.exists():
        st.image(str(timeline_plot_path), width="stretch")
    st.dataframe(
        [
            {
                "episode_index": row["episode_index"],
                "active_strategy": row["active_strategy"],
                "reward": row["reward"],
                "learning_progress": row["learning_progress"],
            }
            for row in episode_metrics
        ],
        width="stretch",
        hide_index=True,
    )


def _render_decision_journal(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Журнал Stay / Switch")
    if selected_experiment_id is None:
        st.info("Спочатку виберіть експеримент.")
        return

    decisions = service.get_decisions(selected_experiment_id, artifacts_root=artifacts_root)
    if not decisions:
        st.info("Рішення ще не зафіксовані.")
        return

    switched_only = st.checkbox("Показувати лише перемикання", value=False, key="switched_only")
    filtered = [row for row in decisions if row["switched"]] if switched_only else decisions
    stay_count = sum(1 for row in decisions if row["action"] == "stay")
    switch_count = sum(1 for row in decisions if row["action"] == "switch")
    col1, col2 = st.columns(2)
    col1.metric("Рішень Stay", stay_count)
    col2.metric("Рішень Switch", switch_count)
    reason_counts: dict[str, int] = {}
    for row in decisions:
        reason_counts[row["reason_code"]] = reason_counts.get(row["reason_code"], 0) + 1
    if reason_counts:
        st.bar_chart(reason_counts)
    st.dataframe(filtered, width="stretch", hide_index=True)


def _render_compare(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    experiments: list[dict[str, Any]],
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Порівняння стратегій і запусків")
    if not experiments:
        st.info("Немає експериментів для порівняння.")
        return

    default_selection = [row["experiment_id"] for row in experiments[:2]]
    if selected_experiment_id and selected_experiment_id not in default_selection:
        default_selection = [selected_experiment_id] + default_selection[:1]
    compare_ids = st.multiselect(
        "Експерименти для порівняння",
        options=[row["experiment_id"] for row in experiments],
        default=default_selection,
        key="compare_experiment_ids",
    )
    if not compare_ids:
        st.info("Виберіть хоча б один експеримент.")
        return

    comparison_rows = service.compare_experiments(compare_ids, artifacts_root=artifacts_root)
    st.dataframe(comparison_rows, width="stretch", hide_index=True)
    reward_values = {row["experiment_id"]: row["reward_mean"] for row in comparison_rows if row["reward_mean"] is not None}
    if reward_values:
        st.bar_chart(reward_values)


def _render_reports_and_export(
    *,
    service: ExperimentApiService,
    artifacts_root: str,
    selected_experiment_id: str | None,
) -> None:
    st.subheader("Звіти та експорт")
    if selected_experiment_id is None:
        st.info("Спочатку виберіть експеримент.")
        return

    details = service.get_experiment(selected_experiment_id, artifacts_root=artifacts_root)
    experiment_row = details["experiment"]
    report_payload = service.get_report(selected_experiment_id, artifacts_root=artifacts_root)

    _render_reproducibility_block(experiment_row)
    st.markdown("Звіт")
    st.markdown(report_payload["report_markdown"])

    artifacts_path = Path(experiment_row["artifacts_path"])
    versions_path = artifacts_path / "versions.json"
    if versions_path.exists():
        st.markdown("Знімок версій")
        st.json(json.loads(versions_path.read_text(encoding="utf-8")), expanded=False)

    artifact_rows = []
    for artifact in details["artifacts"]:
        artifact_rows.append(
            {
                "kind": artifact["kind"],
                "description": artifact["description"],
                "path": artifact["path"],
            }
        )
    supplemental_files = [
        artifacts_path / "config.yaml",
        artifacts_path / "config_hash.txt",
        artifacts_path / "versions.json",
        artifacts_path / "metrics.csv",
        artifacts_path / "window_metrics.csv",
        artifacts_path / "decisions.csv",
        artifacts_path / "events.log",
        artifacts_path / "report.md",
    ]
    for file_path in supplemental_files:
        if file_path.exists() and all(row["path"] != str(file_path) for row in artifact_rows):
            artifact_rows.append({"kind": "FILE", "description": file_path.name, "path": str(file_path)})

    st.markdown("Індекс артефактів для експорту")
    st.dataframe(artifact_rows, width="stretch", hide_index=True)
    for line in _build_report_insights(report_payload["report_markdown"]):
        _render_insight_card(line)


def _render_flash_notice() -> None:
    notice = st.session_state.pop("ui_notice", None)
    if notice is None:
        return
    level = notice.get("level", "info")
    text = str(notice.get("text", ""))
    details = notice.get("details", [])
    if level == "success":
        st.success(text)
    elif level == "warning":
        st.warning(text)
    else:
        st.info(text)
    for line in details:
        st.caption(str(line))


def _render_dataset_lab(
    *,
    dataset_lab_service: DatasetLabService,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
) -> None:
    st.subheader("Студія прогнозування")

    builtins = dataset_lab_service.available_builtin_datasets()
    source_mode = st.radio(
        "Джерело датасету",
        options=["Готовий датасет", "Завантажити CSV", "Вставити CSV"],
        horizontal=True,
        key="dataset_lab_source_mode",
    )
    uploaded_file = None
    pasted_csv = ""
    dataset_name = "uploaded-dataset"
    builtin_payload = None
    builtin_rows = 0
    total_builtin_rows = 0
    if source_mode == "Готовий датасет":
        builtin_col, builtin_info_col = st.columns([1.0, 1.0])
        with builtin_col:
            builtin_id = st.selectbox(
                "Готовий датасет",
                options=[option.dataset_id for option in builtins],
                format_func=lambda dataset_id: _builtin_dataset_label(dataset_id, builtins),
                key="dataset_lab_builtin_id",
            )
            total_builtin_rows = dataset_lab_service.builtin_dataset_row_count(builtin_id)
            if st.session_state.get("dataset_lab_builtin_last_id") != builtin_id:
                st.session_state["dataset_lab_builtin_rows"] = total_builtin_rows
                st.session_state["dataset_lab_builtin_last_id"] = builtin_id
            builtin_rows = int(st.session_state.get("dataset_lab_builtin_rows", total_builtin_rows))
        try:
            builtin_payload = dataset_lab_service.load_builtin_dataset_csv(builtin_id, max_rows=builtin_rows)
        except Exception as exc:
            _render_error_card(
                title="Не вдалося завантажити готовий датасет.",
                detail=str(exc),
                suggestions=(
                    "Спробуйте спочатку меншу кількість рядків.",
                    "Якщо проблема лишається, перейдіть на локальний сценарій через завантаження або вставку CSV.",
                ),
            )
            return
        with builtin_info_col:
            st.markdown(
                f"""
                <div class="section-card">
                    <strong>{builtin_payload.label}</strong><br/>
                    {builtin_payload.description}<br/><br/>
                    Джерело: <strong>{builtin_payload.source_label}</strong><br/>
                    Завантажено рядків: <strong>{builtin_payload.row_count}</strong><br/>
                    Поле для прогнозу: <strong>{builtin_payload.target_column}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        dataset_name = builtin_payload.label
    elif source_mode == "Завантажити CSV":
        uploaded_file = st.file_uploader("CSV-датасет", type=["csv"], key="dataset_lab_file")
        if uploaded_file is not None:
            dataset_name = Path(uploaded_file.name).stem
    else:
        pasted_csv = st.text_area(
            "Вставте CSV-дані",
            value=st.session_state.get(
                "dataset_lab_csv_text",
                "timestamp,value,label\n1,10.0,low\n2,12.5,low\n3,18.1,mid\n4,24.4,mid\n5,31.2,high\n6,39.0,high\n",
            ),
            height=180,
            key="dataset_lab_csv_text",
        )
        dataset_name = st.text_input("Назва датасету", value="pasted-stream", key="dataset_lab_name")

    csv_text = builtin_payload.csv_text if builtin_payload is not None else _dataset_source_text(uploaded_file, pasted_csv)
    if not csv_text:
        _render_warning_card(
            "Щоб почати, завантажте або вставте CSV. Найкраще працює часовий потік із одним target-полем і кількома колонками ознак."
        )
        return

    try:
        schema = dataset_lab_service.peek_csv_schema(csv_text)
    except Exception as exc:
        _render_error_card(
            title="Не вдалося прочитати CSV.",
            detail=str(exc),
            suggestions=(
                "Перевірте, що файл має рядок заголовків.",
                "Використовуйте коми як роздільники.",
                "Переконайтеся, що в кожному рядку однакова кількість колонок.",
            ),
        )
        return

    source_signature = hashlib.md5(f"{dataset_name}\n{csv_text}".encode("utf-8")).hexdigest()
    source_changed = _sync_dataset_lab_state(source_signature)

    columns = schema["columns"]
    default_target = builtin_payload.target_column if builtin_payload is not None else _guess_target_column(columns)
    default_order = builtin_payload.order_column if builtin_payload is not None else _guess_order_column(columns)
    default_task_type = builtin_payload.task_type if builtin_payload is not None else "auto"
    default_policy_name = _recommended_policy_name(builtin_payload.dataset_id if builtin_payload is not None else None, default_task_type)
    if source_changed:
        st.session_state["dataset_lab_target"] = default_target
        st.session_state["dataset_lab_order"] = default_order
        st.session_state["dataset_lab_task_type"] = default_task_type
        st.session_state["dataset_lab_policy_name"] = default_policy_name
        st.session_state["dataset_lab_lag_count"] = 3
        st.session_state["dataset_lab_use_manual_limit"] = False
        if builtin_payload is None:
            st.session_state["dataset_lab_max_rows"] = schema["row_count"]
    target_column = str(st.session_state.get("dataset_lab_target", default_target))
    selected_order = str(st.session_state.get("dataset_lab_order", default_order))
    task_type = str(st.session_state.get("dataset_lab_task_type", default_task_type))
    policy_name = str(st.session_state.get("dataset_lab_policy_name", default_policy_name))
    lag_count = 3
    max_rows = 0

    summary_col, preview_col = st.columns([1.1, 0.9])
    with summary_col:
        st.metric("Target", target_column)
        st.metric("Рядки", schema["row_count"])
    with preview_col:
        st.dataframe(
            [
                {
                    "column": column_name,
                    "role": "поле прогнозу" if column_name == target_column else ("час / порядок" if column_name == selected_order else "вхідна ознака"),
                }
                for column_name in columns
            ],
            width="stretch",
            hide_index=True,
        )

    with st.expander("Розширені налаштування", expanded=False):
        target_column = st.selectbox(
            "Колонка target",
            options=columns,
            index=columns.index(default_target) if default_target in columns else len(columns) - 1,
            key="dataset_lab_target",
        )
        order_options = ["<use current row order>"] + columns
        selected_order = st.selectbox(
            "Колонка порядку",
            options=order_options,
            index=order_options.index(default_order) if default_order in order_options else 0,
            key="dataset_lab_order",
        )
        task_type = st.selectbox(
            "Метод перевірки",
            options=["auto", "regression", "classification"],
            index=["auto", "regression", "classification"].index(default_task_type if default_task_type in {"auto", "regression", "classification"} else "auto"),
            format_func=_task_type_label,
            key="dataset_lab_task_type",
        )
        policy_name = st.selectbox(
            "Adaptive-контролер",
            options=list(dataset_lab_service.available_policy_names()),
            index=list(dataset_lab_service.available_policy_names()).index(policy_name),
            format_func=_policy_label,
            key="dataset_lab_policy_name",
        )
        lag_count = int(st.slider("Кількість лагів", min_value=1, max_value=8, value=3, key="dataset_lab_lag_count"))
        use_manual_limit = st.toggle(
            "Задати ліміт рядків вручну",
            value=False,
            key="dataset_lab_use_manual_limit",
            help="Якщо вимкнено, система аналізує весь доступний потік автоматично.",
        )
        if use_manual_limit:
            max_rows = int(
                st.number_input(
                    "Максимум рядків для replay",
                    min_value=1,
                    value=max(1, schema["row_count"]),
                    step=1,
                    key="dataset_lab_max_rows",
                )
            )
            if builtin_payload is not None:
                builtin_rows = int(
                    st.number_input(
                        "Скільки рядків брати з готового потоку",
                        min_value=1,
                        max_value=total_builtin_rows,
                        value=min(builtin_rows, total_builtin_rows),
                        step=1,
                        key="dataset_lab_builtin_rows",
                    )
                )
        else:
            max_rows = 0
            builtin_rows = total_builtin_rows if builtin_payload is not None else builtin_rows

    manual_col, normalized_col = st.columns([1.0, 1.0])
    with manual_col:
        manual_text = st.text_area(
            "Опишіть рядки для додавання",
            value=st.session_state.get("dataset_lab_manual_text", ""),
            height=140,
            key="dataset_lab_manual_text",
            placeholder=(
                "Приклади:\n"
                "Time=2022-05-21 09:00:00, water_flow_lps=\n"
                "timestamp=11, signal=2.8, target=\n"
                "11,2.8,\n"
            ),
        )
        action_cols = st.columns(2)
        if action_cols[0].button("Інтерпретувати рядки", key="dataset_lab_interpret_rows"):
            try:
                interpretation = dataset_lab_service.interpret_manual_rows(
                    base_csv_text=csv_text,
                    manual_text=manual_text,
                    target_column=target_column,
                )
            except Exception as exc:
                st.session_state["dataset_lab_manual_error"] = {
                    "title": "Не вдалося інтерпретувати введені рядки.",
                    "detail": str(exc),
                    "suggestions": (
                        "Спробуйте формат `key=value` з назвами колонок із поточного датасету.",
                        "Або вкажіть CSV-значення в тому самому порядку, що й у поточній схемі.",
                        "Залишайте target порожнім лише в останньому рядку, який потрібно спрогнозувати.",
                    ),
                }
                st.session_state.pop("dataset_lab_manual_rows_csv", None)
                st.session_state.pop("dataset_lab_manual_preview", None)
                st.session_state.pop("dataset_lab_manual_notes", None)
                st.rerun()
            st.session_state["dataset_lab_manual_rows_csv"] = interpretation.normalized_rows_csv
            st.session_state["dataset_lab_manual_preview"] = list(interpretation.preview_rows)
            st.session_state["dataset_lab_manual_notes"] = list(interpretation.notes)
            st.session_state.pop("dataset_lab_manual_error", None)
            st.rerun()
        if action_cols[1].button("Очистити ручні рядки", key="dataset_lab_clear_rows"):
            for key in (
                "dataset_lab_manual_text",
                "dataset_lab_manual_rows_csv",
                "dataset_lab_manual_preview",
                "dataset_lab_manual_notes",
                "dataset_lab_manual_error",
            ):
                st.session_state.pop(key, None)
            st.rerun()
    with normalized_col:
        manual_error = st.session_state.get("dataset_lab_manual_error")
        if isinstance(manual_error, dict):
            _render_error_card(
                title=str(manual_error.get("title", "Не вдалося інтерпретувати введені рядки.")),
                detail=str(manual_error.get("detail", "")),
                suggestions=tuple(str(item) for item in manual_error.get("suggestions", [])),
            )
        preview_rows = st.session_state.get("dataset_lab_manual_preview")
        if isinstance(preview_rows, list) and preview_rows:
            st.dataframe(preview_rows, width="stretch", hide_index=True)

    normalized_rows_csv = str(st.session_state.get("dataset_lab_manual_rows_csv", ""))
    combined_csv_text = dataset_lab_service.append_manual_rows(base_csv_text=csv_text, normalized_rows_csv=normalized_rows_csv)
    appended_rows = len([line for line in normalized_rows_csv.splitlines() if line.strip()])

    if st.button("Аналізувати датасет і побудувати прогноз", key="dataset_lab_run_button", type="primary"):
        try:
            with st.spinner("Створюється фоновий аналіз датасету..."):
                analysis_row_limit = builtin_rows if builtin_payload is not None else max_rows
                status = dataset_lab_job_service.start_csv_job(
                    dataset_name=dataset_name,
                    csv_text=combined_csv_text,
                    target_column=target_column,
                    task_type=task_type,
                    order_column=None if selected_order == "<use current row order>" else selected_order,
                    lag_count=lag_count,
                    policy_name=policy_name,
                    artifacts_root=artifacts_root,
                    max_rows=analysis_row_limit,
                )
        except Exception as exc:
            st.session_state["dataset_lab_error"] = {
                "title": "Не вдалося перевірити датасет.",
                "detail": str(exc),
                "suggestions": _dataset_error_suggestions(str(exc)),
            }
            st.session_state.pop("dataset_lab_active_job_id", None)
            st.rerun()
        st.session_state.pop("dataset_lab_error", None)
        st.session_state["dataset_lab_active_job_id"] = status.job_id
        st.session_state["selected_dataset_job_id"] = status.job_id
        _request_ui_view("Моніторинг виконання")
        st.session_state["ui_notice"] = {
            "level": "success",
            "text": f"Аналіз для {status.dataset_name} запущено у фоні",
            "details": [f"job_id: {status.job_id}", "Перейдіть у «Моніторинг виконання», щоб бачити прогрес і фінальні метрики."],
        }
        st.rerun()

    error_state = st.session_state.get("dataset_lab_error")
    if isinstance(error_state, dict):
        _render_error_card(
            title=str(error_state.get("title", "The dataset could not be analyzed.")),
            detail=str(error_state.get("detail", "")),
            suggestions=tuple(str(item) for item in error_state.get("suggestions", [])),
        )

    active_job_id = st.session_state.get("dataset_lab_active_job_id")
    if isinstance(active_job_id, str) and active_job_id:
        _render_dataset_lab_launch_status_fragment(
            dataset_lab_job_service=dataset_lab_job_service,
            artifacts_root=artifacts_root,
            job_id=active_job_id,
        )
    _render_dataset_lab_history(dataset_lab_service=dataset_lab_service, artifacts_root=artifacts_root)


def _render_dataset_lab_result(*, result: DatasetLabResult) -> None:
    st.markdown("### Результат перевірки")
    top_metrics = st.columns(6)
    top_metrics[0].metric("Наступний прогноз", result.next_prediction)
    top_metrics[1].metric("Впевненість", f"{result.confidence_label} ({result.prediction_confidence:.2f})")
    top_metrics[2].metric("Різниця проти best fixed", f"{result.delta_vs_best_fixed:+.4f}")
    top_metrics[3].metric("Покриття oracle", f"{result.oracle_capture_ratio * 100.0:.1f}%")
    top_metrics[4].metric("Рядки для аналізу", f"{result.source_rows_used} / {result.source_row_count}")
    top_metrics[5].metric("Ціль прогнозу", _prediction_mode_label(result.prediction_mode))

    coverage_label = "повний потік" if result.source_rows_used >= result.source_row_count else "обрізаний зріз"

    st.markdown(
        f"""
        <div class="hero-card">
            <strong>Короткий підсумок прогнозу.</strong> Завантажений потік оцінено як <strong>{_task_type_label(result.task_type)}</strong>.
            Adaptive-контролер завершився на стратегії <strong>{result.final_strategy}</strong> і побудував наступний прогноз
            для <strong>{result.target_column}</strong>. У цьому запуску використано <strong>{result.source_rows_used}</strong> рядків із <strong>{result.source_row_count}</strong> доступних ({coverage_label}),
            а після підготовки отримано <strong>{result.sample_count}</strong> replay-зразків,
            а прогноз стосується режиму <strong>{_prediction_mode_label(result.prediction_mode).lower()}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col, narrative_col = st.columns([1.15, 0.85])
    with score_col:
        st.markdown("#### Порівняльна таблиця")
        score_rows = [
            {"strategy": "adaptive", "score": result.adaptive_score},
            {"strategy": f"best fixed: {result.best_fixed_strategy}", "score": result.best_fixed_score},
            {"strategy": "oracle upper bound", "score": result.oracle_score},
        ]
        st.dataframe(score_rows, width="stretch", hide_index=True)
        st.bar_chart({row["strategy"]: row["score"] for row in score_rows})
        st.markdown(
            f"""
            <div class="section-card">
                <strong>Наскільки ми близькі до найкращої можливої політики перемикань?</strong><br/>
                Oracle gain над best fixed: <strong>{result.oracle_gain:.4f}</strong><br/>
                Приріст adaptive над best fixed: <strong>{result.delta_vs_best_fixed:.4f}</strong><br/>
                Покрита частка oracle gain: <strong>{result.oracle_capture_ratio * 100.0:.1f}%</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with narrative_col:
        st.markdown("#### Інтерпретація")
        for line in result.interpretation:
            _render_insight_card(line)
        st.markdown("#### Рядок для прогнозу")
        st.dataframe([result.forecast_row_preview], width="stretch", hide_index=True)
        st.markdown("#### Обмеження і зауваження")
        for line in result.caveats:
            _render_warning_card(line)

    with st.expander("Останні adaptive-прогнози", expanded=True):
        st.dataframe(list(result.preview_rows), width="stretch", hide_index=True)

    with st.expander("Прогнози стаціонарних стратегій"):
        st.json(result.next_prediction_by_strategy, expanded=False)

    with st.expander("Завантаження та сирі артефакти"):
        st.code(
            "\n".join(
                [
                    f"input_manifest_path={result.input_manifest_path}",
                    f"summary_json_path={result.summary_json_path}",
                    f"report_md_path={result.report_md_path}",
                    f"decision_csv_path={result.decision_csv_path}",
                    f"score_plot_path={result.score_plot_path}",
                    f"portfolio_plot_path={result.portfolio_plot_path}",
                    f"switch_plot_path={result.switch_plot_path}",
                ]
            ),
            language="text",
        )
        _render_downloads(result)

    plot_cols = st.columns(3)
    for column, plot_path, title in (
        (plot_cols[0], result.score_plot_path, "Порівняння adaptive / best fixed / oracle"),
        (plot_cols[1], result.portfolio_plot_path, "Портфель стаціонарних стратегій"),
        (plot_cols[2], result.switch_plot_path, "Хронологія перемикань"),
    ):
        if plot_path and Path(plot_path).exists():
            with column:
                st.markdown(f"#### {title}")
                st.image(plot_path, width="stretch")

    report_path = Path(result.report_md_path)
    if report_path.exists():
        with st.expander("Детальний звіт аналізу", expanded=True):
            st.markdown(report_path.read_text(encoding="utf-8"))



def _render_dataset_lab_launch_status(status: DatasetLabJobStatus) -> None:
    st.markdown("### Поточний запуск аналізу")
    cols = st.columns(5)
    cols[0].metric("Датасет", status.dataset_name)
    cols[1].metric("Статус", status.status)
    cols[2].metric("Фаза", _dataset_job_phase_label(status.phase))
    cols[3].metric("Прогрес", f"{status.progress * 100.0:.0f}%")
    cols[4].metric("Рядки", f"{status.source_rows_used} / {status.source_row_count}" if status.source_row_count else "ще готується")
    st.progress(status.progress, text=f"{_dataset_job_phase_label(status.phase)}")
    if status.error_message:
        st.error(status.error_message)
    elif status.status == "completed":
        st.success("Аналіз завершено. Відкрийте «Звіти та докази» для повного звіту, графіків і артефактів.")
    else:
        st.info("Аналіз виконується у фоні. Можна переходити між вкладками: виконання не перерветься.")


def _render_live_dataset_job_panel(
    *,
    artifacts_root: str,
    job_id: str,
    full_monitor: bool,
) -> None:
    base_url = get_live_monitor_base_url()
    panel_mode = "full" if full_monitor else "compact"
    html_payload = f"""
    <div id="autorl-live-panel"></div>
    <script>
    const baseUrl = {json.dumps(base_url)};
    const artifactsRoot = {json.dumps(artifacts_root)};
    const jobId = {json.dumps(job_id)};
    const panelMode = {json.dumps(panel_mode)};
    const root = document.getElementById("autorl-live-panel");
    const pollMs = 700;
    const chartState = {{
      startIndex: 0,
      windowSize: null,
      lastLength: 0,
    }};
    function esc(value) {{
      return String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
    }}
    function fmt(value, signed=false) {{
      if (value === null || value === undefined || value === "") return "—";
      const number = Number(value);
      if (!Number.isFinite(number)) return esc(value);
      return `${{signed && number >= 0 ? "+" : ""}}${{number.toFixed(4)}}`;
    }}
    function pct(value) {{
      if (value === null || value === undefined) return "—";
      const number = Number(value);
      if (!Number.isFinite(number)) return "—";
      return `${{(number * 100).toFixed(1)}}%`;
    }}
    function phaseLabel(value) {{
      const mapping = {{
        queued: "У черзі", starting: "Підготовка запуску", loading_builtin_dataset: "Завантаження датасету",
        preparing_dataset: "Підготовка датасету", dataset_prepared: "Дані підготовлено",
        building_strategy_trace: "Побудова трас стратегій", running_adaptive_replay: "Adaptive replay",
        building_report: "Формування звіту", completed: "Завершено", failed: "Помилка"
      }};
      return mapping[value] || esc(value || "—");
    }}
    function polyline(values, color, width, height) {{
      if (!values.length) return "";
      const min = Math.min(...values);
      const max = Math.max(...values);
      const spread = Math.max(1e-9, max - min);
      const points = values.map((value, index) => {{
        const x = values.length === 1 ? 0 : (index / (values.length - 1)) * width;
        const y = height - (((value - min) / spread) * height);
        return `${{x.toFixed(1)}},${{y.toFixed(1)}}`;
      }}).join(" ");
      return `<polyline fill="none" stroke="${{color}}" stroke-width="2.25" points="${{points}}" />`;
    }}
    function clamp(value, min, max) {{
      return Math.max(min, Math.min(max, value));
    }}
    function normalizeChartState(telemetryLength) {{
      if (!telemetryLength) {{
        chartState.startIndex = 0;
        chartState.windowSize = null;
        chartState.lastLength = 0;
        return;
      }}
      if (!chartState.windowSize) {{
        chartState.windowSize = telemetryLength;
      }}
      chartState.windowSize = clamp(chartState.windowSize, 12, telemetryLength);
      const maxStart = Math.max(0, telemetryLength - chartState.windowSize);
      if (telemetryLength > chartState.lastLength && chartState.startIndex === Math.max(0, chartState.lastLength - chartState.windowSize)) {{
        chartState.startIndex = maxStart;
      }} else {{
        chartState.startIndex = clamp(chartState.startIndex, 0, maxStart);
      }}
      chartState.lastLength = telemetryLength;
    }}
    function setChartWindow(nextWindow, telemetryLength) {{
      if (!telemetryLength) return;
      const oldWindow = chartState.windowSize || telemetryLength;
      const center = chartState.startIndex + Math.floor(oldWindow / 2);
      chartState.windowSize = clamp(nextWindow, 12, telemetryLength);
      const maxStart = Math.max(0, telemetryLength - chartState.windowSize);
      chartState.startIndex = clamp(center - Math.floor(chartState.windowSize / 2), 0, maxStart);
      chartState.lastLength = telemetryLength;
    }}
    function shiftChart(direction, telemetryLength) {{
      if (!telemetryLength) return;
      const step = Math.max(1, Math.floor((chartState.windowSize || telemetryLength) * 0.25));
      const maxStart = Math.max(0, telemetryLength - (chartState.windowSize || telemetryLength));
      chartState.startIndex = clamp(chartState.startIndex + direction * step, 0, maxStart);
      chartState.lastLength = telemetryLength;
    }}
    function resetChart(telemetryLength) {{
      chartState.windowSize = telemetryLength || null;
      chartState.startIndex = 0;
      chartState.lastLength = telemetryLength || 0;
    }}
    function buildChart(telemetry) {{
      if (!telemetry.length) return "";
      normalizeChartState(telemetry.length);
      const visibleTelemetry = telemetry.slice(chartState.startIndex, chartState.startIndex + chartState.windowSize);
      const width = 760;
      const height = 180;
      const adaptive = visibleTelemetry.map(row => Number(row.adaptive_score_so_far || 0));
      const bestFixed = visibleTelemetry.map(row => Number(row.best_fixed_score_so_far || 0));
      const delta = visibleTelemetry.map(row => Number(row.delta_so_far || 0));
      const endIndex = chartState.startIndex + visibleTelemetry.length;
      const isFullWindow = visibleTelemetry.length === telemetry.length;
      return `<div class="section"><div class="section-title">Живий хід adaptive replay</div><div class="chart-toolbar"><div class="chart-range">${{isFullWindow ? "Повний діапазон" : `Точки ${{chartState.startIndex + 1}}–${{endIndex}} з ${{telemetry.length}}`}}</div><div class="chart-actions"><button type="button" data-action="pan-left" class="chart-btn" title="Ліворуч">←</button><button type="button" data-action="zoom-out" class="chart-btn" title="Зменшити масштаб">−</button><button type="button" data-action="zoom-in" class="chart-btn" title="Збільшити масштаб">+</button><button type="button" data-action="pan-right" class="chart-btn" title="Праворуч">→</button><button type="button" data-action="zoom-reset" class="chart-btn chart-btn-reset" title="Скинути масштаб">Скинути</button></div></div><svg viewBox="0 0 ${{width}} ${{height}}" class="chart">${{polyline(adaptive, "#0f766e", width, height)}}${{polyline(bestFixed, "#1d4ed8", width, height)}}${{polyline(delta, "#b45309", width, height)}}</svg><div class="legend"><span><i style="background:#0f766e"></i>adaptive</span><span><i style="background:#1d4ed8"></i>best fixed</span><span><i style="background:#b45309"></i>delta</span></div></div>`;
    }}
    function buildTelemetryTable(telemetry) {{
      if (!telemetry.length) return "";
      const rows = telemetry.slice(-12).reverse().map(row => `<tr><td>${{esc(row.sample_index || "")}}</td><td>${{esc(row.evaluation_index || "")}}</td><td>${{esc(row.active_strategy || "—")}}</td><td>${{esc(row.candidate_strategy || "—")}}</td><td>${{fmt(row.adaptive_score_so_far)}}</td><td>${{fmt(row.best_fixed_score_so_far)}}</td><td>${{fmt(row.delta_so_far, true)}}</td><td>${{pct(row.oracle_capture_so_far)}}</td></tr>`).join("");
      return `<div class="section"><div class="section-title">Останні telemetry точки</div><table class="grid"><thead><tr><th>sample</th><th>eval</th><th>active</th><th>candidate</th><th>adaptive</th><th>best fixed</th><th>delta</th><th>oracle</th></tr></thead><tbody>${{rows}}</tbody></table></div>`;
    }}
    function buildJobsTable(jobs) {{
      if (!jobs.length || panelMode !== "full") return "";
      const rows = jobs.slice(0, 10).map(job => `<tr><td>${{esc(job.dataset_name || "")}}</td><td>${{esc(job.status || "")}}</td><td>${{phaseLabel(job.phase || "")}}</td><td>${{(Number(job.progress || 0) * 100).toFixed(0)}}%</td><td>${{esc(job.active_strategy || "—")}}</td><td>${{fmt(job.delta_vs_best_fixed, true)}}</td></tr>`).join("");
      return `<div class="section"><div class="section-title">Інші фонові аналізи</div><table class="grid"><thead><tr><th>датасет</th><th>статус</th><th>фаза</th><th>прогрес</th><th>active</th><th>delta</th></tr></thead><tbody>${{rows}}</tbody></table></div>`;
    }}
    function render(status, telemetry, jobs) {{
      const progress = Math.max(0, Math.min(100, Math.round(Number(status.progress || 0) * 100)));
      const completed = status.status === "completed";
      const failed = status.status === "failed";
      root.innerHTML = `<style>:root{{color-scheme:light;font-family:"Segoe UI",Tahoma,sans-serif;}}body{{margin:0;background:transparent;}}.panel{{color:#0f172a;background:#ffffff;border:1px solid #dbe3ee;border-radius:18px;padding:16px;box-shadow:0 8px 24px rgba(15,23,42,.05);}}.headline{{font-size:20px;font-weight:700;margin-bottom:12px;}}.grid-cards{{display:grid;grid-template-columns:repeat(${{panelMode === "full" ? 6 : 5}},minmax(0,1fr));gap:10px;margin-bottom:12px;}}.card{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;padding:10px 12px;}}.label{{font-size:12px;color:#64748b;margin-bottom:4px;}}.value{{font-size:16px;font-weight:700;color:#0f172a;}}.progress-shell{{width:100%;height:12px;border-radius:999px;background:#e2e8f0;overflow:hidden;margin:12px 0 6px;}}.progress-bar{{height:100%;width:${{progress}}%;background:linear-gradient(90deg,#163247 0%,#0f766e 100%);}}.status-text{{font-size:13px;color:#475569;margin-bottom:12px;}}.section{{margin-top:16px;}}.section-title{{font-size:15px;font-weight:700;margin-bottom:8px;}}.chart{{width:100%;height:auto;background:#f8fafc;border:1px solid #e2e8f0;border-radius:14px;display:block;}}.chart-toolbar{{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px;}}.chart-range{{font-size:12px;color:#475569;font-weight:600;}}.chart-actions{{display:flex;gap:6px;flex-wrap:wrap;}}.chart-btn{{appearance:none;border:1px solid #cbd5e1;background:#ffffff;color:#0f172a;border-radius:10px;padding:4px 10px;font-size:12px;font-weight:700;cursor:pointer;line-height:1.2;}}.chart-btn:hover{{background:#f8fafc;}}.chart-btn:active{{background:#e2e8f0;}}.chart-btn-reset{{padding-inline:12px;}}.legend{{display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;color:#475569;font-size:12px;}}.legend i{{width:10px;height:10px;display:inline-block;border-radius:999px;margin-right:6px;vertical-align:middle;}}.grid{{width:100%;border-collapse:collapse;font-size:12px;}}.grid th,.grid td{{text-align:left;padding:8px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;}}.grid th{{color:#475569;font-weight:600;background:#f8fafc;}}.message{{margin-top:12px;padding:10px 12px;border-radius:12px;font-size:13px;}}.message.ok{{background:#ecfdf5;color:#166534;border:1px solid #bbf7d0;}}.message.err{{background:#fef2f2;color:#991b1b;border:1px solid #fecaca;}}.message.run{{background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;}}</style><div class="panel"><div class="headline">${{panelMode === "full" ? "Моніторинг виконання" : "Поточний запуск аналізу"}}</div><div class="grid-cards"><div class="card"><div class="label">Датасет</div><div class="value">${{esc(status.dataset_name || "—")}}</div></div><div class="card"><div class="label">Статус</div><div class="value">${{esc(status.status || "—")}}</div></div><div class="card"><div class="label">Фаза</div><div class="value">${{phaseLabel(status.phase || "")}}</div></div><div class="card"><div class="label">Рядки</div><div class="value">${{status.source_row_count ? `${{status.source_rows_used}} / ${{status.source_row_count}}` : "—"}}</div></div><div class="card"><div class="label">Контролер</div><div class="value">${{esc(status.policy_name || status.active_strategy || "—")}}</div></div>${{panelMode === "full" ? `<div class="card"><div class="label">Перемикання</div><div class="value">${{esc(status.switch_count || 0)}}</div></div>` : ""}}</div><div class="progress-shell"><div class="progress-bar"></div></div><div class="status-text">Прогрес: <strong>${{progress}}%</strong> · sample: <strong>${{status.total_samples ? `${{status.sample_index}} / ${{status.total_samples}}` : "—"}}</strong> · active: <strong>${{esc(status.active_strategy || "—")}}</strong> · candidate: <strong>${{esc(status.candidate_strategy || "—")}}</strong></div>${{panelMode === "full" ? `<div class="grid-cards"><div class="card"><div class="label">Adaptive зараз</div><div class="value">${{fmt(status.adaptive_score_so_far)}}</div></div><div class="card"><div class="label">Best fixed зараз</div><div class="value">${{fmt(status.best_fixed_score_so_far)}}</div></div><div class="card"><div class="label">Delta зараз</div><div class="value">${{fmt(status.delta_so_far, true)}}</div></div><div class="card"><div class="label">Oracle зараз</div><div class="value">${{pct(status.oracle_capture_so_far)}}</div></div><div class="card"><div class="label">Adaptive фінально</div><div class="value">${{fmt(status.adaptive_score)}}</div></div><div class="card"><div class="label">Best fixed фінально</div><div class="value">${{fmt(status.best_fixed_score)}}</div></div></div>` : ""}}${{buildChart(telemetry)}}${{buildTelemetryTable(telemetry)}}${{buildJobsTable(jobs)}}${{failed ? `<div class="message err">${{esc(status.error_message || "Помилка виконання")}}</div>` : completed ? `<div class="message ok">Аналіз завершено. Повний звіт уже доступний у вкладці «Звіти та докази».</div>` : `<div class="message run">Аналіз виконується у фоні. Оновлюється лише цей блок, без перемальовування всієї сторінки.</div>`}}</div>`;
    }}
    root.addEventListener("click", (event) => {{
      const button = event.target.closest("[data-action]");
      if (!button) return;
      const action = button.getAttribute("data-action");
      if (action === "zoom-in") {{
        setChartWindow(Math.floor((chartState.windowSize || chartState.lastLength || 48) * 0.65), chartState.lastLength);
      }} else if (action === "zoom-out") {{
        setChartWindow(Math.ceil((chartState.windowSize || chartState.lastLength || 48) * 1.5), chartState.lastLength);
      }} else if (action === "pan-left") {{
        shiftChart(-1, chartState.lastLength);
      }} else if (action === "pan-right") {{
        shiftChart(1, chartState.lastLength);
      }} else if (action === "zoom-reset") {{
        resetChart(chartState.lastLength);
      }}
      refresh();
    }});
    root.addEventListener("wheel", (event) => {{
      const chart = event.target.closest(".chart");
      if (!chart || !chartState.lastLength) return;
      event.preventDefault();
      if (event.deltaY < 0) {{
        setChartWindow(Math.floor((chartState.windowSize || chartState.lastLength) * 0.8), chartState.lastLength);
      }} else {{
        setChartWindow(Math.ceil((chartState.windowSize || chartState.lastLength) * 1.25), chartState.lastLength);
      }}
      refresh();
    }}, {{ passive: false }});
    async function refresh() {{
      try {{
        const query = `artifacts_root=${{encodeURIComponent(artifactsRoot)}}&job_id=${{encodeURIComponent(jobId)}}`;
        const [statusResp, telemetryResp, jobsResp] = await Promise.all([
          fetch(`${{baseUrl}}/dataset-lab/job-status?${{query}}`, {{ cache: "no-store" }}),
          fetch(`${{baseUrl}}/dataset-lab/telemetry?${{query}}&limit=240`, {{ cache: "no-store" }}),
          fetch(`${{baseUrl}}/dataset-lab/jobs?artifacts_root=${{encodeURIComponent(artifactsRoot)}}&limit=20`, {{ cache: "no-store" }})
        ]);
        const status = await statusResp.json();
        const telemetry = telemetryResp.ok ? await telemetryResp.json() : [];
        const jobs = jobsResp.ok ? await jobsResp.json() : [];
        render(status, Array.isArray(telemetry) ? telemetry : [], Array.isArray(jobs) ? jobs : []);
        const terminal = ["completed", "failed"].includes(String(status.status || ""));
        window.setTimeout(refresh, terminal ? 3000 : pollMs);
      }} catch (error) {{
        root.innerHTML = `<div style="padding:12px;border:1px solid #fecaca;background:#fef2f2;color:#991b1b;border-radius:12px;font-family:Segoe UI,Tahoma,sans-serif;">Не вдалося оновити live-монітор: ${{esc(error && error.message ? error.message : error)}}</div>`;
        window.setTimeout(refresh, 1500);
      }}
    }}
    refresh();
    </script>
    """
    components.html(html_payload, height=980 if full_monitor else 720, scrolling=False)


def _render_dataset_lab_launch_status_fragment(
    *,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
    job_id: str,
) -> None:
    try:
        dataset_lab_job_service.get_job_status(job_id, artifacts_root=artifacts_root)
    except FileNotFoundError:
        return
    _render_live_dataset_job_panel(artifacts_root=artifacts_root, job_id=job_id, full_monitor=False)


def _render_dataset_lab_history(*, dataset_lab_service: DatasetLabService, artifacts_root: str) -> None:
    history_rows = dataset_lab_service.list_dataset_lab_analyses(artifacts_root=artifacts_root, limit=12)
    if not history_rows:
        return
    st.markdown("### Останні збережені аналізи")
    table_rows = [
        {
            "час": row.get("created_at_utc", ""),
            "датасет": row.get("dataset_name", ""),
            "режим": row.get("task_type", ""),
            "контролер": row.get("policy_name", ""),
            "рядки": f"{row.get('source_rows_used', 0)} / {row.get('source_row_count', 0)}",
            "replay": row.get("sample_count", 0),
            "adaptive": row.get("adaptive_score", 0.0),
            "delta": row.get("delta_vs_best_fixed", 0.0),
            "oracle_capture_%": float(row.get("oracle_capture_ratio", 0.0)) * 100.0,
            "switches": row.get("switch_count", 0),
        }
        for row in history_rows
    ]
    st.dataframe(table_rows, width="stretch", hide_index=True)
    latest = history_rows[0]
    latest_report_path = Path(str(latest.get("report_md_path", "")))
    if latest_report_path.exists():
        with st.expander("Останній детальний звіт із історії", expanded=False):
            st.markdown(latest_report_path.read_text(encoding="utf-8"))


def _render_dataset_lab_monitor(
    *,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
) -> None:
    st.subheader("Фонові аналізи датасетів")
    jobs = dataset_lab_job_service.list_jobs(artifacts_root=artifacts_root, limit=20)
    if not jobs:
        st.info("Фонових аналізів датасетів ще немає. Запустіть аналіз у «Студії прогнозування».")
        return
    options = [job.job_id for job in jobs]
    current = st.session_state.get("selected_dataset_job_id")
    if current not in options:
        current = options[0]
    selected_job_id = st.selectbox("Запуск аналізу для перегляду", options=options, index=options.index(current), key="selected_dataset_job_id")
    _render_live_dataset_job_panel(artifacts_root=artifacts_root, job_id=selected_job_id, full_monitor=True)


def _render_dataset_lab_evidence(
    *,
    dataset_lab_service: DatasetLabService,
    dataset_lab_job_service: DatasetLabJobService,
    artifacts_root: str,
) -> None:
    st.subheader("Звіти аналізів датасетів")
    jobs = dataset_lab_job_service.list_jobs(artifacts_root=artifacts_root, limit=30)
    completed_jobs = [job for job in jobs if job.status == "completed" and job.summary_json_path]
    if not completed_jobs:
        st.info("Завершених аналізів датасетів ще немає.")
        return
    options = [job.job_id for job in completed_jobs]
    current = st.session_state.get("selected_dataset_job_id")
    if current not in options:
        current = options[0]
    selected_job_id = st.selectbox("Збережений аналіз", options=options, index=options.index(current), key="dataset_evidence_job_id")
    st.session_state["selected_dataset_job_id"] = selected_job_id
    result = dataset_lab_job_service.load_completed_result(selected_job_id, artifacts_root=artifacts_root)
    history = dataset_lab_service.list_dataset_lab_analyses(artifacts_root=artifacts_root, limit=20)
    compare_rows = [
        {
            "час": row.get("created_at_utc", ""),
            "датасет": row.get("dataset_name", ""),
            "контролер": row.get("policy_name", ""),
            "adaptive": row.get("adaptive_score", 0.0),
            "delta": row.get("delta_vs_best_fixed", 0.0),
            "oracle_capture_%": float(row.get("oracle_capture_ratio", 0.0)) * 100.0,
            "перемикання": row.get("switch_count", 0),
        }
        for row in history
    ]
    if compare_rows:
        st.markdown("#### Порівняння останніх аналізів")
        st.dataframe(compare_rows, width="stretch", hide_index=True)
    _render_dataset_lab_result(result=result)


def _render_builtin_dataset_spotlight(artifacts_root: str) -> None:
    st.markdown("### Огляд benchmark-датасетів")
    st.caption(
        "Для відтворюваних демонстрацій застосунок уже має підготовлені нестаціонарні потоки, зокрема WaterFlow, Airlines "
        "та InsectsRecurring, у benchmark replay-шарі."
    )
    benchmark_root = Path(artifacts_root) / "real_stream_validation"
    if benchmark_root.exists():
        st.code(f"benchmark_artifacts_root={benchmark_root}", language="text")


def _dataset_source_text(uploaded_file, pasted_csv: str) -> str:
    if uploaded_file is not None:
        payload = uploaded_file.getvalue()
        if isinstance(payload, bytes):
            return payload.decode("utf-8", errors="replace")
        return str(payload)
    return pasted_csv


def _render_insight_card(text: str) -> None:
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)


def _render_warning_card(text: str) -> None:
    st.markdown(f'<div class="warning-card">{text}</div>', unsafe_allow_html=True)


def _render_error_card(*, title: str, detail: str, suggestions: tuple[str, ...]) -> None:
    st.markdown(
        f"""
        <div class="warning-card">
            <strong>{title}</strong><br/>
            {detail}
        </div>
        """,
        unsafe_allow_html=True,
    )
    for suggestion in suggestions:
        _render_insight_card(suggestion)


def _render_downloads(result: DatasetLabResult) -> None:
    summary_path = Path(result.summary_json_path)
    report_path = Path(result.report_md_path)
    if summary_path.exists():
        st.download_button(
            "Завантажити summary JSON",
            data=summary_path.read_text(encoding="utf-8"),
            file_name=summary_path.name,
            mime="application/json",
            key=f"download-summary-{result.dataset_name}",
        )
    if report_path.exists():
        st.download_button(
            "Завантажити Markdown-звіт",
            data=report_path.read_text(encoding="utf-8"),
            file_name=report_path.name,
            mime="text/markdown",
            key=f"download-report-{result.dataset_name}",
        )
    for label, path_value in (
        ("Завантажити графік score comparison", result.score_plot_path),
        ("Завантажити графік fixed portfolio", result.portfolio_plot_path),
        ("Завантажити графік switch timeline", result.switch_plot_path),
    ):
        artifact_path = Path(path_value)
        if artifact_path.exists():
            st.download_button(
                label,
                data=artifact_path.read_bytes(),
                file_name=artifact_path.name,
                mime="image/png",
                key=f"download-{artifact_path.name}-{result.dataset_name}",
            )


def _task_type_label(value: str) -> str:
    mapping = {
        "auto": "Автовизначення за значеннями target",
        "regression": "Прогнозування / регресія",
        "classification": "Класифікація",
    }
    return mapping.get(value, value)


def _guess_target_column(columns: list[str]) -> str:
    lowered = {column.lower(): column for column in columns}
    for candidate in ("target", "label", "class", "y", "value", "approval", "water_flow_lps", "bikes_in_use", "price_up"):
        if candidate in lowered:
            return lowered[candidate]
    return columns[-1]


def _guess_order_column(columns: list[str]) -> str:
    lowered = {column.lower(): column for column in columns}
    for candidate in ("timestamp", "time", "datetime", "date", "moment", "ordinal_date", "period"):
        if candidate in lowered:
            return lowered[candidate]
    return "<use current row order>"


def _recommended_policy_name(dataset_profile: str | None, task_type: str) -> str:
    _ = dataset_profile
    _ = task_type
    return "auto_meta"


def _prediction_mode_label(value: str) -> str:
    mapping = {
        "manual_row": "Доданий рядок",
        "next_step": "Наступний невідомий крок",
    }
    return mapping.get(value, value)


def _policy_label(value: str) -> str:
    mapping = {
        "auto_meta": "Автовибір найкращого контролера",
        "recent_leader_meta": "Мета-контролер recent leader",
        "hard_switch_lcb": "LCB-контролер жорсткого перемикання",
        "fixed_share_portfolio": "Fixed-share портфель",
        "best_fixed_guard": "Захист best fixed",
    }
    return mapping.get(value, value)


def _dataset_job_phase_label(value: str) -> str:
    mapping = {
        "queued": "У черзі",
        "starting": "Підготовка запуску",
        "loading_builtin_dataset": "Завантаження готового датасету",
        "preparing_dataset": "Підготовка датасету",
        "dataset_prepared": "Дані підготовлено",
        "building_strategy_trace": "Побудова трас стратегій",
        "running_adaptive_replay": "Adaptive replay",
        "building_report": "Формування звіту та графіків",
        "completed": "Завершено",
        "failed": "Помилка",
    }
    return mapping.get(value, value)


def _format_metric_value(value: float | None, *, signed: bool = False) -> str:
    if value is None:
        return "-"
    if signed:
        return f"{value:+.4f}"
    return f"{value:.4f}"


def _dataset_error_suggestions(message: str) -> tuple[str, ...]:
    lowered = message.lower()
    if "too short" in lowered:
        return (
            "Додайте більше рядків. Replay потребує достатньої історії після побудови лагів, щоб порівняти adaptive і fixed стратегії.",
            "Зменште кількість лагів, якщо датасет короткий.",
            "Для швидкого тесту бажано мати хоча б 10-15 рядків після впорядкування.",
        )
    if "header" in lowered:
        return (
            "Переконайтеся, що перший рядок містить назви колонок.",
            "Використовуйте звичайний CSV із комами як роздільниками.",
        )
    if "target column" in lowered or "order column" in lowered:
        return (
            "Ще раз перевірте вибрані колонки target і порядку.",
            "Переконайтеся, що схема CSV відповідає налаштуванням вище.",
        )
    return (
        "Перевірте, що CSV має стабільний заголовок і достатню кількість рядків.",
        "Якщо target є часовим, переконайтеся, що обраний порядок рядків відповідає часу.",
    )


def _builtin_dataset_label(dataset_id: str, builtins: tuple[Any, ...]) -> str:
    match = next((item for item in builtins if item.dataset_id == dataset_id), None)
    if match is None:
        return dataset_id
    return f"{match.label}  |  {match.description}"


def _request_ui_view(view: str) -> None:
    st.session_state["pending_ui_view"] = view


def _sync_dataset_lab_state(source_signature: str) -> bool:
    if st.session_state.get("dataset_lab_source_signature") == source_signature:
        return False
    for key in (
        "dataset_lab_error",
        "dataset_lab_manual_rows_csv",
        "dataset_lab_manual_preview",
        "dataset_lab_manual_notes",
        "dataset_lab_manual_error",
    ):
        st.session_state.pop(key, None)
    st.session_state["dataset_lab_source_signature"] = source_signature
    return True


def _build_experiment_insights(
    experiment_row: dict[str, Any],
    episode_metrics: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> tuple[str, ...]:
    lines = [
        (
            f"Експеримент `{experiment_row['experiment_name']}` зараз перебуває у статусі `{experiment_row['status']}` "
            f"із seed `{experiment_row['seed']}`."
        )
    ]
    if episode_metrics:
        mean_reward = sum(row["reward"] for row in episode_metrics) / len(episode_metrics)
        lines.append(f"Середня зафіксована винагорода наразі становить `{mean_reward:.4f}` на `{len(episode_metrics)}` епізодах.")
        lines.append(
            f"Остання активна стратегія — `{episode_metrics[-1]['active_strategy']}`, а її недавня винагорода дорівнює `{episode_metrics[-1]['reward']:.4f}`."
        )
    if decisions:
        switch_count = sum(1 for row in decisions if row["switched"])
        lines.append(f"Контролер виконав `{switch_count}` реальних перемикань серед `{len(decisions)}` перевірених рішень.")
    else:
        lines.append("Рядки рішень метаконтролера ще не зафіксовані.")
    return tuple(lines)


def _build_report_insights(report_markdown: str) -> tuple[str, ...]:
    lines = []
    if "Switch decisions" in report_markdown or "switch_count" in report_markdown:
        lines.append("Звіт містить докази перемикань, тому його можна використовувати для пояснення, коли і чому контролер змінив стратегію.")
    if "config_hash" in report_markdown:
        lines.append("Звіт уже містить контекст відтворюваності й може використовуватися як зручний артефакт для аудиту.")
    return tuple(lines)


def _progress_text(status: str, current_episode: int | None, total_episodes: int | None) -> str:
    if total_episodes is None:
        return f"статус={status}"
    if current_episode is None:
        return f"статус={status} | очікування першого збереженого епізоду"
    return f"статус={status} | епізод {current_episode + 1} / {total_episodes}"


def _maybe_auto_refresh(status: str) -> None:
    return


def _render_reproducibility_block(experiment_row: dict[str, Any]) -> None:
    artifacts_path = Path(experiment_row["artifacts_path"])
    versions_path = artifacts_path / "versions.json"
    st.markdown("Відтворюваність")
    st.code(
        "\n".join(
            [
                f"seed={experiment_row['seed']}",
                f"config_hash={experiment_row['config_hash']}",
                f"artifacts_path={experiment_row['artifacts_path']}",
                f"versions_path={versions_path}",
            ]
        ),
        language="text",
    )


def _build_config_payload(
    *,
    experiment_name: str,
    mode: str,
    scenario_name: str,
    seed: int,
    episodes: int,
    steps_per_episode: int,
    fixed_action_index: int,
    selected_strategy_names: list[str],
    window_size: int,
    min_samples: int,
    delta: float,
    lambda_value: float,
    switch_cost: float,
    temperature: float,
    notes: str,
    artifacts_root: str,
) -> dict[str, Any]:
    strategy_names = selected_strategy_names or ["fixed"]
    return {
        "schema_version": "1.0",
        "experiment_name": experiment_name,
        "seed": seed,
        "mode": mode,
        "scenario": {
            "name": scenario_name,
            "episodes": episodes,
            "steps_per_episode": steps_per_episode,
            "tags": ["ui", "phase9", scenario_name],
            "description": "Streamlit-created experiment.",
        },
        "strategies": [
            _build_strategy_payload(
                strategy_name=name,
                fixed_action_index=fixed_action_index,
                temperature=temperature,
            )
            for name in strategy_names
        ],
        "meta_controller": {
            "window_size": window_size,
            "min_samples": min_samples,
            "delta": delta,
            "lambda": lambda_value,
            "switch_cost": switch_cost,
            "utility_weights": {
                "reward_mean": 1.0,
                "reward_variance": 0.0,
                "compute_cost": 0.0,
                "switch_cost": 0.0,
            },
        },
        "artifacts_root": artifacts_root,
        "tags": ["ui", "phase9", mode],
        "notes": notes,
    }


def _build_strategy_payload(*, strategy_name: str, fixed_action_index: int, temperature: float) -> dict[str, Any]:
    compute_costs = {
        "fixed": 0.05,
        "greedy_reward": 0.08,
        "drift_aware": 0.12,
        "lcb_conservative": 0.11,
        "tempered_reward": 0.14,
        "adaptive_meta": 0.20,
    }
    parameters: dict[str, Any] = {}
    if strategy_name == "fixed":
        parameters["fixed_action_index"] = fixed_action_index
    if strategy_name in {"tempered_reward", "adaptive_meta"}:
        parameters["temperature"] = temperature
    return {
        "name": strategy_name,
        "parameters": parameters,
        "compute_cost": compute_costs[strategy_name],
    }


if __name__ == "__main__":
    main()
