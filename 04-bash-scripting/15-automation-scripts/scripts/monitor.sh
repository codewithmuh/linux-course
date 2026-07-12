#!/usr/bin/env bash
# monitor.sh — print a single-line health snapshot, ideal for appending to a
# log file from cron:
#   * * * * * /path/to/monitor.sh >> /var/log/monitor.log
# Usage: ./monitor.sh
set -euo pipefail

now=$(date +%F_%T)
load=$(uptime | awk -F'load average:' '{print $2}' | sed 's/^ *//')
mem=$(free | awk '/Mem:/{printf "%.0f%%", $3/$2*100}')
disk=$(df / | awk 'END{print $5}')

echo "$now load=$load mem=$mem disk=$disk"
