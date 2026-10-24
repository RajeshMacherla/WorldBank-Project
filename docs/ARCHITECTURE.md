# Architecture and implemented boundaries

Browser → loopback HTTP API → bounded orchestrator → safety filter → retrieval tool → request-check tool → generator → citation validator → SQLite review queue.

Offline and Local AI modes use a fixed plan. Agentic AI uses a bounded model-selected tool loop in app/agents.py followed by structured generation and validation. The model chooses approved search and procurement tools. This is a single-agent workflow, not an autonomous multi-agent system. SQLite stores run/session history; history is not injected into prompts. Human review outcomes are recorded separately and never approve transactions.

Demo mode uses keyword overlap and extractive passages. AI mode uses Ollama /api/embed, a content/model-keyed local embedding cache, cosine retrieval, and /api/chat with a JSON schema. No Chroma dependency is needed for this small corpus. The generator is asked for exact quotations; the application validates IDs and quotations and renders cited claims only. Quotations do not establish semantic entailment; reviewers must check whether claims follow from evidence.

Documents are trusted, repository-controlled synthetic Markdown. Chunk IDs include source, paragraph and word offset. Pages are not claimed. Change documents only while the app is stopped. The app has no file upload, OCR, live vendor integration, authentication, role-based authorization, autonomous subagents, or enterprise deployment. Tool inputs are entered in the form rather than extracted by the model.

## Operational behavior

HTTP is bound to 127.0.0.1. Host validation and a per-process browser token protect mutations from simple cross-origin requests. One mutation runs at a time. Inputs and body sizes are bounded. Ollama calls have timeouts and one retry. Invalid model output escalates. Model unavailability is reported as a service error rather than silently pretending an AI answer succeeded.

Request traces include workflow nodes and elapsed times. JSONL operational logs contain IDs and timings, not raw prompts. SQLite DOES store evidence and generated output; do not use confidential material. The review queue is shared by all users of this local process. Session history is queryable by ID; it is not an authorization boundary.

## Azure mapping

azure-pipelines.yml validates and packages the app; hosted-agent availability must be checked. No cloud deployment has been executed. events.jsonl maps conceptually to custom events; latency maps to request duration; review/error counts map to custom metrics. Application Insights and Azure Monitor exporters are not implemented. Do not describe this as deployed Azure observability. A future exporter should use OpenTelemetry, redact payloads, and be opt-in because ingestion can incur charges.

## Extension milestones

1. Add document upload with size/type checks, isolated parsing, and explicit classification.
2. Add FastAPI and schema-generated OpenAPI contracts.
3. Optionally migrate the tested bounded agent loop to LangGraph for checkpointing.
4. Add a second specialist only if evaluations show it improves quality.
5. Add OpenTelemetry traces and an optional Azure Monitor exporter.
6. Add authentication and authorization before hosting or multi-user use.
