# ADR-002: Clean Architecture with Hexagonal Pattern

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Dr.Confluence-group

---

## Context

The system has three distinct interface modes (CLI, GUI, web), multiple capture backends (live, PCAP file), and multiple storage formats. Without a clear architectural pattern, these concerns would become tightly coupled, making testing and extension difficult.

## Decision

Adopt Clean Architecture with a Hexagonal (Ports and Adapters) pattern.

## Rationale

- **Testability:** The domain and use case layers have zero external dependencies, enabling fast, isolated unit tests without mocking network interfaces or file systems.
- **Extensibility:** New capture backends, storage formats, and UI modes can be added by implementing port interfaces without touching the domain.
- **Maintainability:** Clear layer boundaries prevent accidental coupling. A solo maintainer can reason about each layer independently.
- **Open-source readiness:** Contributors can work on a single adapter without understanding the entire system.

## Alternatives Considered

| Pattern | Reason Rejected |
|---|---|
| Layered (MVC) | Tight coupling between UI and business logic; hard to test |
| Event-driven only | Increases complexity for a tool that is primarily request-response |
| Monolithic script | Not scalable; impossible to test; not suitable for open-source |

## Consequences

- **Positive:** High testability; clear extension points; maintainable by solo developer
- **Negative:** More initial boilerplate than a simple script; steeper learning curve for new contributors
- **Mitigation:** Comprehensive documentation and examples; ADRs explain the rationale
