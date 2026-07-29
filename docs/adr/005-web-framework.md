# ADR-005: FastAPI + HTMX for Web Dashboard

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Dr.Confluence-group

---

## Context

The web dashboard needs to:
- Serve a real-time packet analysis interface in a browser
- Support WebSocket for live packet streaming
- Be lightweight (this is a local tool, not a web application)
- Require minimal JavaScript build tooling
- Be accessible (WCAG 2.1 AA)

## Decision

Use FastAPI for the backend and HTMX + Alpine.js for the frontend, with Chart.js for charts.

## Rationale

- **FastAPI:** Async-native; built-in WebSocket support; automatic OpenAPI documentation; Pydantic integration for request/response validation.
- **HTMX:** Server-driven interactivity without a JavaScript build step. The dashboard is a local tool — a full SPA framework (React, Vue) would add unnecessary complexity.
- **Alpine.js:** Minimal reactive state management for UI interactions that HTMX doesn’t cover. 15 KB minified.
- **Chart.js:** Lightweight; no build step; good real-time update support via `update()` API.

## Alternatives Considered

| Technology | Reason Rejected |
|---|---|
| Django | Overkill; ORM and admin not needed; slower startup |
| Flask | No async; no built-in WebSocket; less ergonomic |
| React SPA | Build toolchain complexity; overkill for a local dashboard |
| Vue SPA | Same as React |
| Streamlit | Limited customization; not suitable for real-time packet display |

## Consequences

- **Positive:** Minimal JS complexity; fast development; auto-documented API
- **Negative:** HTMX is less familiar than React to some contributors
- **Mitigation:** HTMX documentation is excellent; examples provided in the codebase
