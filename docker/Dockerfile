# PacketSnifferAnalyzer — Docker Development Environment
#
# This Dockerfile creates a development environment with all dependencies
# pre-installed. It does NOT include the GUI (PyQt6) — use the host for GUI.
#
# Build: docker build -f docker/Dockerfile -t psa-dev .
# Run:   docker compose up -d

FROM python:3.11-slim AS base

LABEL maintainer="dr-confluence-group"
LABEL description="PacketSnifferAnalyzer development environment"
LABEL version="0.1.0-alpha.1"

# Install system dependencies for libpcap
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap-dev \
    libpcap0.8 \
    tcpdump \
    iproute2 \
    iputils-ping \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for running the application
# Note: capture still requires NET_RAW capability (granted via docker-compose)
RUN groupadd --gid 1000 psa && \
    useradd --uid 1000 --gid psa --shell /bin/bash --create-home psa

WORKDIR /app

# Install Python dependencies first (layer caching)
COPY requirements/base.txt requirements/base.txt
COPY requirements/dev.txt requirements/dev.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/dev.txt

# Copy project source
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e ".[dev]"

# =============================================================================
# Production stage (minimal, no dev tools)
# =============================================================================
FROM python:3.11-slim AS production

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 psa && \
    useradd --uid 1000 --gid psa --shell /bin/bash --create-home psa

WORKDIR /app

COPY requirements/prod.txt requirements/prod.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/prod.txt

COPY --from=base /app/src ./src
COPY --from=base /app/pyproject.toml ./pyproject.toml
COPY --from=base /app/README.md ./README.md
COPY --from=base /app/LICENSE ./LICENSE

RUN pip install --no-cache-dir -e . && \
    chown -R psa:psa /app

USER psa

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8080/health || exit 1

CMD ["psa", "dashboard", "start", "--host", "127.0.0.1", "--port", "8080"]
