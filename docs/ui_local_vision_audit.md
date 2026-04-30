# Local Vision Audit

This audit used a local multimodal model and real browser screenshots, not only text snapshots.

## Setup

- screenshots captured from the running Streamlit UI with Selenium + Chrome
- screenshot artifacts:
  - `artifacts/ui_local_vision_review/forecast_initial.png`
  - `artifacts/ui_local_vision_review/operations_monitor.png`
  - `artifacts/ui_local_vision_review/evidence.png`
  - `artifacts/ui_local_vision_review/forecast_result.png`
  - `artifacts/ui_local_vision_review/contact_sheet.png`
- local model used:
  - `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`
- automation entrypoint:
  - `scripts/local_vision_ui_review.py`

## Local Model Signal

The local vision model was useful for broad signal, but not reliable enough for nuanced product judgment.

Useful signal:
- it consistently flagged the UI as not commercially usable
- it detected density/readability problems
- it detected that the error state is confusing

Weak signal:
- the stronger 2.2B run produced generic hallucinated claims such as security and downtime issues that are not visually grounded
- therefore the final verdict must be anchored in the screenshots, not in raw model prose alone

## Grounded Findings

### Forecast Studio

- the page still behaves like an internal lab, not like a forecasting product
- `Selected experiment` is shown above the main forecast workflow, even though it is irrelevant for a user who just wants to upload data and get a prediction
- the vertical space is used poorly: the page opens with a large hero, large whitespace, and a benchmark block, while the primary forecasting action sits lower than it should
- the left sidebar is overloaded with technical state such as artifacts root and AI env-var guidance instead of task-oriented actions
- the page does not clearly answer the first user question: "what do I do first?"

### Error State

- the error state is unacceptable for a product UI
- the user sees a raw Python traceback inside the main page
- there is no human explanation of what went wrong
- there is no recovery guidance such as minimum required rows, expected schema, or a one-click example fix
- this alone is enough to say the UI is not production-ready

### Operations Monitor

- the monitor is visually more structured than Forecast Studio, but it is still too engineering-heavy
- `Selected experiment` and `Run to inspect` duplicate each other and waste attention
- the action row gives nearly equal visual weight to `Start`, `Stop`, `Rerun`, and `Refresh`, which is unsafe for operator UX
- the screen is overloaded with metrics, repeated summary cards, reproducibility data, and event logs in one long scroll
- the operator does not get a single dominant status summary like:
  - healthy / unstable / degraded
  - current risk
  - recommended next action

### Evidence Page

- the evidence page is readable for an internal researcher, but not for a business user
- raw hashes, paths, and detailed report content appear too early
- the page lacks a concise executive summary before technical evidence

## Verdict

The current UI is still not commercially usable.

The biggest blockers are:
- wrong information hierarchy
- product-critical error handling failure
- too much repository and experiment management leaking into the user flow
- not enough decision-oriented guidance for either forecasting users or operators

## Next Redesign Priority

1. Remove experiment-centric controls from `Forecast Studio`.
2. Replace raw traceback rendering with product error cards.
3. Put the forecasting CTA and schema guidance above the fold.
4. Split operator state into `status`, `risk`, `recommended action`, and `evidence`.
5. Move hashes, artifact paths, and deep technical logs behind secondary disclosure.
