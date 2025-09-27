# Multi-Agent Financial Research Orchestrator — Initial Commit (Structure Only)

This is the skeleton commit. It includes folders, empty modules, and docs so you can understand the layout before adding code.

### What's here
- `dags/` — placeholder Airflow DAG file
- `ingest/` — placeholders for EDGAR + RSS fetchers
- `models/` — embedding interface placeholder
- `retriever/` — FAISS and Qdrant client placeholders
- `ui/` — Streamlit app placeholder
- `orchestrator/` — Kafka/Temporal/Workers placeholders
- `indices/` — empty; where FAISS artifacts will live later
- `docs/` — architecture notes + roadmap
- `docker-compose.yml` — commented skeleton so you see intended services
- `.github/workflows/build_index.example.yml` — commented example workflow (disabled)

See `ROADMAP.md` for how to grow this into a working demo.
