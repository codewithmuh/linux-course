#!/usr/bin/env bash
# healthcheck.sh — check CPU load, memory, and disk against thresholds.
# Prints a WARN line for anything over its limit and exits non-zero if any
# threshold is breached, so cron can gate an alert on the exit code.
# Usage: ./healthcheck.sh
#   Thresholds (percent) can be overridden via environment variables:
#     CPU_MAX=85 MEM_MAX=90 DISK_MAX=80 ./healthcheck.sh
set -euo pipefail

CPU_MAX="${CPU_MAX:-85}"
MEM_MAX="${MEM_MAX:-90}"
DISK_MAX="${DISK_MAX:-80}"

breach=0

# Disk: percent used on the root filesystem.
disk=$(df / | awk 'END{print $5}' | tr -d '%')
if [[ "$disk" -gt "$DISK_MAX" ]]; then
  echo "WARN disk ${disk}% (max ${DISK_MAX}%)"
  breach=1
fi

# Memory: used / total as a percentage.
mem=$(free | awk '/Mem:/{printf "%.0f", $3/$2*100}')
if [[ "$mem" -gt "$MEM_MAX" ]]; then
  echo "WARN mem ${mem}% (max ${MEM_MAX}%)"
  breach=1
fi

# CPU: 1-minute load average as a percentage of the available cores.
cores=$(nproc)
load1=$(awk '{print $1}' /proc/loadavg)
cpu=$(awk -v l="$load1" -v c="$cores" 'BEGIN{printf "%.0f", (l/c)*100}')
if [[ "$cpu" -gt "$CPU_MAX" ]]; then
  echo "WARN cpu ${cpu}% (max ${CPU_MAX}%)"
  breach=1
fi

if [[ "$breach" -eq 0 ]]; then
  echo "OK cpu ${cpu}% mem ${mem}% disk ${disk}%"
fi

exit "$breach"
