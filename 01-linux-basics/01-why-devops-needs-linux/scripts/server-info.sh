#!/usr/bin/env bash
# server-info.sh — a one-glance snapshot of any Linux box.
# Usage: ./server-info.sh
set -euo pipefail

echo "Host:    $(hostname)"
echo "Kernel:  $(uname -sr)"
if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  echo "Distro:  $(. /etc/os-release && echo "${PRETTY_NAME:-unknown}")"
fi
echo "User:    $(whoami)"
echo "Uptime:  $(uptime -p 2>/dev/null || uptime)"
