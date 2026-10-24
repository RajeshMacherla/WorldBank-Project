# Policy & Procurement Risk Assistant

A local AI engineering portfolio project: policy retrieval, structured cited answers, deterministic procurement checks, human review and repeatable evaluations. All policies and vendors are fictional. No World Bank affiliation, endorsement or compliance claim.

## Start now — no package installation

Prerequisite: Python 3.11+ and a browser. Your existing Python 3.15 can run the standard-library app.

```bash
cd policy-risk-assistant
python3 -m app.server
```

Open http://127.0.0.1:8000 and select **Offline demo**. The default request demonstrates missing bidding justification and required senior approval. Demo mode uses keyword retrieval and extracts passages; it does not use an LLM. Stop with Ctrl+C. If port 8000 is occupied: `python3 -m app.server --port 8001`.

## Enable local AI — free model inference

1. Install Ollama from https://ollama.com/download/mac and open it.
2. In Terminal, download the models (internet and several GB of disk space required):

```bash
ollama pull qwen2.5:3b
ollama pull nomic-embed-text
ollama list
```

3. Restart the app and select **Local AI**. The first request builds the local embedding cache. Keep Ollama running. If its service is not running, run `ollama serve` in a separate Terminal; do not start a second server if the desktop app already serves it.

A 3B model is a starting choice for an Apple Silicon laptop; speed and available memory need checking on your machine. To choose a smaller chat model, pull it and start with `OLLAMA_MODEL=your-model-name python3 -m app.server`. No paid API key, AWS account, Azure subscription, Docker, VS Code or pip packages are required for this release. Model downloads require accepting their applicable licenses.

## Verify

From the project folder:

```bash
python3 -m unittest discover -s tests -v
python3 -m scripts.evaluate
python3 -m scripts.evaluate --mode ai
```

The last command needs Ollama and downloaded models. Demo results do not measure AI quality. Evaluation contains four curated retrieval cases plus basic safety/abstention checks. For answer accuracy, manually grade a held-out set with expected evidence before making claims.

## Included

- Browser interface and local HTTP API.
- Markdown ingestion, overlapping chunks, source/section/classification metadata.
- Local embeddings and cosine retrieval in AI mode; keyword baseline in demo mode.
- Schema-constrained generation and exact-quote validation.
- Fixed-plan coordinator, policy-check tools, synthetic vendor lookup.
- SQLite session history and human review queue.
- Node timings, redacted operational event logs, error handling.
- Unit tests, evaluation harness, GitHub Actions and Azure Pipelines validation/packaging configuration.

See [architecture](docs/ARCHITECTURE.md), [learning guide](docs/LEARNING_GUIDE.md), and [security boundaries](docs/SECURITY.md).

## API

`GET /health` reports local server health (not model readiness). `GET /api/reviews` returns the local review queue. `GET /api/history?session=ID` returns recent runs. `POST /api/run` accepts question, mode, session and optional request `{amount, vendor_id, bidding_justification}`. `POST /api/review` accepts run_id, status (acknowledged or needs_follow_up), and note. Mutation endpoints require the per-process X-App-Token provided to the browser. Use the UI for the initial demo; this is not an authenticated enterprise API.

## GitHub preparation

Review files and keep .runtime/, credentials, personal data, virtual environments and model binaries out of Git. Upload the CONTENTS of this project folder as the repository root so .github/workflows/ci.yml is recognized. If adding it under a subfolder, adjust CI working directories and workflow location first. Do not initialize a nested Git repository inside an existing checkout. A GitHub push publishes source code, not a live AI service. Add screenshots and a short video after running your local AI demonstration.

## Implementation status

Working standard-library baseline with optional Ollama integration. AI inference must be verified after local models are installed. Agentic AI mode adds a bounded model-selected tool loop. There are no autonomous subagents, LangGraph, FastAPI, OpenTelemetry exporter, Azure cloud deployment, real institutional API, PDF ingestion or production security claims. Azure pipeline YAML is supplied but has not been executed against an Azure DevOps organization.

## Agentic AI mode

Select Agentic AI in the mode menu. The coordinator model selects search_policy and check_procurement calls, receives their results and can make another call before finishing. A separate structured generation stage produces the cited answer. The runner permits at most three model rounds and six tool calls. It verifies that evidence exists and that submitted procurement was checked; otherwise it escalates. The model cannot change form values. Expand the workflow trace to see agent_tool events. Twenty mocked/offline tests pass; live model tool-calling performance still requires local verification. No additional installation is needed beyond the two Ollama models.
