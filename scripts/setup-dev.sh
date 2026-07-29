#!/usr/bin/env bash
# scripts/setup-dev.sh
#
# Sets up the development environment for PacketSnifferAnalyzer.
# Run this script once after cloning the repository.
#
# Usage: bash scripts/setup-dev.sh

set -euo pipefail

echo "==> PacketSnifferAnalyzer — Development Environment Setup"
echo ""

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MINOR" -lt 10 ]; then
    echo "ERROR: Python 3.10 or later is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "==> Python $PYTHON_VERSION detected"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "==> Creating virtual environment..."
    python -m venv .venv
else
    echo "==> Virtual environment already exists"
fi

# Activate virtual environment
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip
echo "==> Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "==> Installing development dependencies..."
pip install -e ".[dev]" --quiet

# Install pre-commit hooks
echo "==> Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg

# Check for libpcap
if command -v dpkg &> /dev/null; then
    if ! dpkg -l libpcap-dev &> /dev/null; then
        echo ""
        echo "WARNING: libpcap-dev not found. Install with:"
        echo "  sudo apt-get install libpcap-dev"
    fi
elif command -v brew &> /dev/null; then
    echo "==> macOS detected. libpcap is included with Xcode Command Line Tools."
fi

echo ""
echo "==> Setup complete!"
echo ""
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  make check          # Run all checks"
echo "  psa --version       # Verify installation"
echo "  psa interfaces      # List network interfaces (may require sudo)"
