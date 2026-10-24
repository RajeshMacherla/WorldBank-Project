# Learn the project in six sessions

1. Run offline mode. Read data/policies and change the amount from 9999 to 10000 and 50000. Explain the difference between retrieval and a deterministic business rule.
2. Read chunks() and retrieve(). Print chunk IDs, inspect metadata, and compare broad and specific questions. Explain keyword retrieval versus vector similarity.
3. Install Ollama and download the two models. Run AI mode and inspect citations. Explain why embeddings retrieve while the chat model generates.
4. Read SYSTEM, SCHEMA, validate_output(), and run(). Try an injection phrase and a made-up question. Explain why a valid quote alone does not guarantee a correct claim.
5. Run tests and evaluation. Add one policy and one held-out question. Manually grade correctness, evidence support and missing information; do not report unmeasured accuracy.
6. Read server.py and the CI files. Trace one request from browser through tools to SQLite. Explain local deployment, CI packaging, and the steps still needed for secure cloud hosting.

## Five-minute demo

Start in demo mode and explain it is not an LLM. Run the default 75000-dollar request; show bidding and senior-approval findings. Change vendor to V002 and inspect the review queue. Record needs_follow_up with a note. Switch to AI mode after installing models, ask a policy question, and show quoted evidence and node timings. Show tests, the evaluation report and architecture limitations.

## Honest interview description

I built a local policy review prototype with two execution modes. The AI path uses local embeddings and a local LLM to generate structured, cited claims. I added deterministic policy tools, citation validation, session persistence, human review and a repeatable evaluation harness. Agentic AI mode adds model-selected tools with bounded execution. Autonomous subagents and Azure telemetry are future extensions.
