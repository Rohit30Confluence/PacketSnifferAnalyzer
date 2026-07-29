#!/usr/bin/env bash
# scripts/check-privileges.sh
#
# Checks whether the current user has sufficient privileges for packet capture.
# Provides platform-specific remediation instructions.
#
# Usage: bash scripts/check-privileges.sh

set -euo pipefail

echo "==> PacketSnifferAnalyzer — Privilege Check"
echo ""

OS=$(uname -s)

case "$OS" in
    Linux)
        echo "Platform: Linux"
        if [ "$(id -u)" -eq 0 ]; then
            echo "Status: PASS (running as root)"
        else
            echo "Status: CHECKING capabilities..."
            if command -v getcap &> /dev/null; then
                PYTHON_PATH=$(which python)
                CAPS=$(getcap "$PYTHON_PATH" 2>/dev/null || echo "none")
                if echo "$CAPS" | grep -q "cap_net_raw"; then
                    echo "Status: PASS (CAP_NET_RAW granted to $PYTHON_PATH)"
                else
                    echo "Status: FAIL"
                    echo ""
                    echo "Remediation options:"
                    echo "  1. Run with sudo: sudo psa capture start ..."
                    echo "  2. Grant capabilities:"
                    echo "     sudo setcap cap_net_raw,cap_net_admin+eip $PYTHON_PATH"
                    echo "  3. Use Docker with --cap-add NET_RAW"
                fi
            else
                echo "Status: UNKNOWN (getcap not available)"
                echo "Install libcap2-bin: sudo apt-get install libcap2-bin"
            fi
        fi
        ;;
    Darwin)
        echo "Platform: macOS"
        if [ "$(id -u)" -eq 0 ]; then
            echo "Status: PASS (running as root)"
        else
            echo "Status: FAIL"
            echo "Remediation: Run with sudo: sudo psa capture start ..."
        fi
        ;;
    *)
        echo "Platform: $OS (unsupported for this check)"
        echo "On Windows, run from an Administrator terminal."
        ;;
esac

echo ""
echo "==> Scapy interface detection:"
python -c "from scapy.all import get_if_list; ifaces = get_if_list(); print(f'Detected {len(ifaces)} interface(s): {ifaces}')"
