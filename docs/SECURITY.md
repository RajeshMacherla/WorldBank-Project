# Security and Responsible AI

Use synthetic public data only. No World Bank data, employer documents, credentials, or personal data belong in this repository. Rules and vendor records are fictional; they are not World Bank policy.

Implemented controls: loopback binding, host checks, token-protected mutations, limited body sizes, fixed local model endpoint, schema and citation validation, constrained deterministic tools, no execution tools, basic injection-pattern screening and human review.

Known limitations: pattern matching is easy to bypass; content filtering is incomplete; LLMs can misinterpret evidence; there is no identity management or authorization; outputs and evidence persist in plaintext SQLite. Local model inference is not proof of regulatory compliance. Synthetic tests do not establish production safety.

Delete .runtime/ while the server is stopped to reset local data. That folder is excluded from Git. Do not expose this server through tunnels, port forwarding or public hosting. A production design needs authentication, authorization, encrypted storage, retention controls, stronger document isolation and an organization-specific security review.
