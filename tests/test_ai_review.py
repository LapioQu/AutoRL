"""External AI review service tests."""

from __future__ import annotations

from autorl.application.ai_review import OpenAIReviewService, _extract_manual_rows_json, _fallback_output_text


def test_openai_review_service_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("AI_REVIEW_API_KEY", raising=False)
    service = OpenAIReviewService()

    assert service.configured is False
    try:
        service._complete("hello")
    except RuntimeError as exc:
        assert "AI_REVIEW_API_KEY" in str(exc)
    else:
        raise AssertionError("expected missing-key runtime error")


def test_openai_review_service_uses_groq_defaults(monkeypatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.delenv("AI_REVIEW_PROVIDER", raising=False)
    monkeypatch.delenv("AI_REVIEW_MODEL", raising=False)
    monkeypatch.delenv("AI_REVIEW_ENDPOINT", raising=False)
    monkeypatch.delenv("OPENAI_REVIEW_MODEL", raising=False)

    service = OpenAIReviewService()

    assert service.configured is True
    assert service.provider == "groq"
    assert service.model == "openai/gpt-oss-20b"


def test_fallback_output_text_reads_message_content() -> None:
    payload = {
        "output": [
            {
                "content": [
                    {"text": "First paragraph."},
                    {"text": "Second paragraph."},
                ]
            }
        ]
    }

    assert _fallback_output_text(payload) == "First paragraph.\nSecond paragraph."


def test_extract_manual_rows_json_parses_plain_json_payload() -> None:
    rows = _extract_manual_rows_json(
        '[{"timestamp":"11","signal":"2.8","target":""}]',
        ("timestamp", "signal", "target"),
    )

    assert rows == ({"timestamp": "11", "signal": "2.8", "target": ""},)
