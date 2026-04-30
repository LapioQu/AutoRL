# DOC-02 DFD Level 0

```mermaid
flowchart LR
    cfg[Config / CSV / Built-in Dataset] --> orch[Experiment Orchestrator / Dataset Lab]
    orch --> env[Environment / Replay Stream]
    env --> strategies[Strategy Portfolio]
    strategies --> metrics[Metrics Collector]
    metrics --> eval[Evaluator]
    eval --> meta[MetaController]
    meta --> logs[Decisions / Events / Reports]
    metrics --> logs
    orch --> store[(SQLite + Artifact Store)]
    logs --> store
    store --> api[FastAPI]
    store --> cli[CLI]
    store --> ui[Streamlit UI]
```

Основний потік:
- конфігурація або дані подаються в application layer;
- runtime збирає метрики;
- evaluator і metacontroller формують рішення;
- результати зберігаються в SQLite та файлових артефактах;
- CLI/API/UI читають один і той самий persisted state.
