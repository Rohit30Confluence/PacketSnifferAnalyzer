"""FastAPI web dashboard application.

The web dashboard provides a real-time browser-based interface with:
  - Live packet stream via WebSocket
  - Real-time charts (packets/sec, protocol distribution)
  - Top-talkers table
  - Flow table with pagination
  - Capture controls
  - Prometheus-compatible /metrics endpoint
  - /health endpoint

Security:
  - Binds to 127.0.0.1 by default (configurable with warning)
  - No packet payload data is exposed via the API
  - CORS is restricted to localhost origins

This module is a scaffold. The full implementation will be added
in Milestone 5 (Epic 6).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="PacketSnifferAnalyzer Dashboard",
    description="Real-time network traffic analysis dashboard.",
    version="0.1.0-alpha.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS: restrict to localhost origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Operations"])
async def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        A JSON object with status 'ok' when the server is running.
    """
    return {"status": "ok", "version": "0.1.0-alpha.1"}


@app.get("/metrics", tags=["Operations"])
async def metrics() -> str:
    """Prometheus-compatible metrics endpoint.

    Returns:
        Metrics in Prometheus text exposition format.
    """
    # Full implementation in Phase 3 — M5
    return "# PacketSnifferAnalyzer metrics\n# Full implementation in Phase 3 (M5)\n"


# Routers will be registered in Phase 3 — M5
# from packetanalyzer.interfaces.web.routers import sessions, statistics, flows
# app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
# app.include_router(statistics.router, prefix="/api/statistics", tags=["Statistics"])
# app.include_router(flows.router, prefix="/api/flows", tags=["Flows"])
