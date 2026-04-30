"""External AI review integration for forecasting and UX critique."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any
import urllib.error
import urllib.request

from autorl.application.dataset_lab import DatasetLabResult


@dataclass(frozen=True, slots=True)
class AIReviewResult:
    """One external-AI review output."""

    review_kind: str
    model: str
    content_markdown: str


class OpenAIReviewService:
    """Call an external OpenAI model for interpretation and UX critique."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        endpoint: str | None = None,
    ) -> None:
        self._provider = _resolve_provider(provider)
        self._api_key = _resolve_api_key(api_key, self._provider)
        self._model = model or os.environ.get("AI_REVIEW_MODEL", "").strip() or os.environ.get("OPENAI_REVIEW_MODEL", "").strip() or _default_model(self._provider)
        self._endpoint = endpoint or os.environ.get("AI_REVIEW_ENDPOINT", "").strip() or _default_endpoint(self._provider)

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    @property
    def provider(self) -> str:
        return self._provider

    @property
    def model(self) -> str:
        return self._model

    def review_dataset_result(self, result: DatasetLabResult) -> AIReviewResult:
        """Explain one forecast in plain language for an operational user."""
        prompt = "\n".join(
            [
                "Ти аналізуєш результат прогнозування для операційного бізнес-користувача.",
                "Напиши стислий markdown українською мовою з такими розділами:",
                "## Прогноз простою мовою",
                "## Чому система так вважає",
                "## Фактори ризику",
                "## Рекомендована наступна дія",
                "",
                "Відповідь має бути конкретною, практичною і зрозумілою для людини без ML-бекграунду.",
                "Не згадуй prompt engineering або приховані міркування.",
                "",
                f"task_type: {result.task_type}",
                f"target_column: {result.target_column}",
                f"next_prediction: {result.next_prediction}",
                f"confidence_label: {result.confidence_label}",
                f"prediction_confidence: {result.prediction_confidence:.4f}",
                f"adaptive_score: {result.adaptive_score:.4f}",
                f"best_fixed_strategy: {result.best_fixed_strategy}",
                f"best_fixed_score: {result.best_fixed_score:.4f}",
                f"delta_vs_best_fixed: {result.delta_vs_best_fixed:.4f}",
                f"final_strategy: {result.final_strategy}",
                f"switch_count: {result.switch_count}",
                f"interpretation_lines: {json.dumps(list(result.interpretation), ensure_ascii=True)}",
                f"caveats: {json.dumps(list(result.caveats), ensure_ascii=True)}",
                f"next_prediction_by_strategy: {json.dumps(result.next_prediction_by_strategy, ensure_ascii=True)}",
            ]
        )
        return AIReviewResult(
            review_kind="forecast_explanation",
            model=self._model,
            content_markdown=self._complete(prompt),
        )

    def review_forecast_studio_ux(self, result: DatasetLabResult) -> AIReviewResult:
        """Ask the model to critique whether the forecast workflow is commercially usable."""
        prompt = "\n".join(
            [
                "Ти суворий senior product designer, який оцінює застосунок для прогнозування.",
                "Оціни сценарій Студії прогнозування з точки зору комерційної придатності на основі контексту нижче.",
                "Відповідай українською у форматі markdown з такими розділами:",
                "## Що вже працює добре",
                "## Що досі шкодить UX",
                "## Чого бракує реальним користувачам",
                "## Найпріоритетніші виправлення",
                "",
                "Будь конкретним. Фокусуйся на зрозумілості, довірі, підтримці рішень і придатності сценарію для користувача, який хоче отримати прогноз.",
                "",
                "Поточні можливості Студії прогнозування:",
                "- завантаження або вставка CSV",
                "- вибір target і колонки порядку",
                "- автоматичне визначення типу задачі",
                "- вибір adaptive-політики",
                "- прогноз наступного кроку",
                "- індикатор впевненості",
                "- прогнози допоміжних стратегій",
                "- завантаження артефактів",
                "",
                f"current_result_summary: {json.dumps({'task_type': result.task_type, 'target_column': result.target_column, 'next_prediction': result.next_prediction, 'confidence_label': result.confidence_label, 'delta_vs_best_fixed': result.delta_vs_best_fixed, 'switch_count': result.switch_count}, ensure_ascii=True)}",
            ]
        )
        return AIReviewResult(
            review_kind="forecast_studio_ux",
            model=self._model,
            content_markdown=self._complete(prompt),
        )

    def review_run_monitor(self, payload: dict[str, Any]) -> AIReviewResult:
        """Explain one adaptive run and critique monitor usefulness."""
        prompt = "\n".join(
            [
                "Ти оцінюєш операційну панель adaptive online-learning системи.",
                "Напиши markdown українською з такими розділами:",
                "## Операційне читання ситуації",
                "## Цінність для прийняття рішень",
                "## UX-проблеми, що лишаються",
                "## Рекомендовані дії оператора",
                "",
                "Використовуй структурований payload нижче. Сфокусуйся на тому, чи може оператор зрозуміти, що відбувається прямо зараз.",
                json.dumps(payload, ensure_ascii=True, sort_keys=True, default=str),
            ]
        )
        return AIReviewResult(
            review_kind="run_monitor_review",
            model=self._model,
            content_markdown=self._complete(prompt),
        )

    def interpret_manual_rows(self, *, columns: tuple[str, ...], target_column: str, manual_text: str) -> tuple[dict[str, str], ...]:
        """Use an external model to coerce free-text row descriptions into the active schema."""
        prompt = "\n".join(
            [
                "Ти приводиш ручно введені рядки для прогнозування до схеми CSV-датасету.",
                "Поверни тільки валідний JSON.",
                "Відповідь має бути JSON-масивом з одного або більше об'єктів.",
                "Кожен об'єкт має використовувати лише такі точні ключі і концептуально зберігати цей порядок:",
                json.dumps(list(columns), ensure_ascii=True),
                f"Якщо target `{target_column}` невідомий і має бути спрогнозований, поверни його як порожній рядок.",
                "Не додавай пояснень, markdown-блоків або зайвих ключів.",
                "Текст ручного вводу:",
                manual_text,
            ]
        )
        response_text = self._complete(prompt)
        return _extract_manual_rows_json(response_text, columns)

    def _complete(self, prompt: str) -> str:
        if not self.configured:
            raise RuntimeError(
                "Не налаштовано ключ зовнішнього ШІ API. Вкажіть AI_REVIEW_API_KEY або використайте OPENAI_API_KEY / GROQ_API_KEY."
            )

        body = {
            "model": self._model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ],
                }
            ],
        }
        request = urllib.request.Request(
            self._endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"{self._provider} review request failed: HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{self._provider} review request failed: {exc.reason}") from exc

        output_text = payload.get("output_text")
        if output_text:
            return str(output_text)
        return _fallback_output_text(payload)


def _fallback_output_text(payload: dict[str, Any]) -> str:
    """Extract text from a Responses API payload if output_text is absent."""
    output_items = payload.get("output", [])
    parts: list[str] = []
    for item in output_items:
        for content_item in item.get("content", []):
            text_value = content_item.get("text")
            if text_value:
                parts.append(str(text_value))
    if parts:
        return "\n".join(parts)
    raise RuntimeError("OpenAI review response did not contain textual output.")


def _extract_manual_rows_json(payload_text: str, columns: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    """Parse a strict JSON row payload returned by an external model."""
    candidate = payload_text.strip()
    if "```" in candidate:
        segments = [segment.strip() for segment in candidate.split("```") if segment.strip()]
        json_like = next((segment.removeprefix("json").strip() for segment in segments if segment.lstrip().startswith("[") or segment.lstrip().startswith("{") or segment.lower().startswith("json")), "")
        if json_like:
            candidate = json_like

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Зовнішній ШІ не повернув валідний JSON для ручних рядків: {exc}") from exc

    items = payload if isinstance(payload, list) else [payload]
    rows: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            raise RuntimeError("Зовнішній ШІ повернув рядок не у форматі об'єкта.")
        row = {column: str(item.get(column, "")) for column in columns}
        extra_keys = sorted(set(item.keys()) - set(columns))
        if extra_keys:
            raise RuntimeError(f"Зовнішній ШІ повернув неочікувані ключі: {', '.join(extra_keys)}")
        rows.append(row)
    if not rows:
        raise RuntimeError("Зовнішній ШІ не повернув жодного рядка.")
    return tuple(rows)


def _resolve_provider(provider: str | None) -> str:
    candidate = provider or os.environ.get("AI_REVIEW_PROVIDER", "").strip() or ("groq" if os.environ.get("GROQ_API_KEY", "").strip() else "openai")
    normalized = candidate.strip().lower()
    return normalized if normalized in {"openai", "groq"} else "openai"


def _resolve_api_key(api_key: str | None, provider: str) -> str:
    if api_key:
        return api_key
    generic = os.environ.get("AI_REVIEW_API_KEY", "").strip()
    if generic:
        return generic
    if provider == "groq":
        return os.environ.get("GROQ_API_KEY", "").strip()
    return os.environ.get("OPENAI_API_KEY", "").strip()


def _default_model(provider: str) -> str:
    if provider == "groq":
        return "openai/gpt-oss-20b"
    return "gpt-5.5"


def _default_endpoint(provider: str) -> str:
    if provider == "groq":
        return "https://api.groq.com/openai/v1/responses"
    return "https://api.openai.com/v1/responses"
