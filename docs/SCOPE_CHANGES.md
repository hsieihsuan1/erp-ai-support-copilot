# Scope changes from the original project

## Retained and adapted

- ERP URL/module/page pattern tables from the original extension. Hostname detection now parses URLs and checks domain boundaries rather than searching the whole URL string. Included for review and regression tests, not activated against real ERP pages by the demo manifest.
- Original RAG chunking approach. Added parameter bounds and terminal-chunk handling to guarantee loop progress. Used by tests; the local demo retrieves complete synthetic runbooks instead of chunked embeddings.
- In-context support, structured response and escalation workflow concepts.
- ServiceNow/Jira provider names and mock interface idea. Their HTTP clients were not copied.

## Rewritten for the demo

- FastAPI app and request models, public demo identity mapping, tenant/principal ownership checks, server-created session IDs and in-memory state.
- Sidebar UI and synthetic ERP screen. No copy of the original admin/dashboard pages, logos or deployed UI assets.
- Lexical retrieval over three newly written synthetic records, two tenants and two modules.
- Mock ticket providers and transcript confirmation. No provider URLs or credentials.
- Manifest restricted to the local demo route, plus an explicit user-opened sidebar.
- API tests, URL tests, release checks and actual-extension browser smoke test.

## Deliberately excluded

- All portfolio Git history, original zip archives and packaged extension downloads.
- Uploaded documents, knowledge files, database material, wallets, logs, client records and deployment configuration.
- Cloud identifiers, live endpoints, personal domains, email addresses and operational credentials.
- Live Oracle/Gemini clients, PDF/document ingestion workers, authentication/JWT code, admin routes, dashboards and ticket-provider HTTP code.
- Broad page permissions, automatic screen capture, automatic error text transmission and automatic ticket creation.
- Unverified claims of reduced ticket volume, production readiness, broad ERP support and score-based reliability.

## Why this is narrower than the original

The original chat path uses optional authentication. Its in-memory session store is keyed only by a caller-supplied session ID, and its JWT service has a hardcoded fallback secret. The reviewed RAG query combines company rows with a shared global document pool. None of those facts establishes a tested cross-tenant incident, but they prevent treating the original source as production-isolation evidence.

The demo makes principal ownership checks testable without bringing those deployment paths or private data into the release. Public demo aliases are intentionally not represented as real authentication. A real auth boundary and database-level isolation still need implementation and review.
