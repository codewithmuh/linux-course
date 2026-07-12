#!/usr/bin/env bash
# logclean.sh — keep a log directory tidy:
#   - gzip *.log files older than 7 days
#   - delete *.gz archives older than 30 days
# Usage: ./logclean.sh [log-dir]
set -euo pipefail

LOG_DIR="${1:-/var/log/myapp}"
COMPRESS_AFTER=7    # days
DELETE_AFTER=30     # days

if [[ ! -d "$LOG_DIR" ]]; then
  echo "log directory not found: $LOG_DIR" >&2
  exit 1
fi

echo "Compressing *.log older than ${COMPRESS_AFTER}d in $LOG_DIR"
find "$LOG_DIR" -type f -name "*.log" -mtime "+${COMPRESS_AFTER}" -exec gzip {} \;

echo "Deleting *.gz older than ${DELETE_AFTER}d in $LOG_DIR"
find "$LOG_DIR" -type f -name "*.gz" -mtime "+${DELETE_AFTER}" -delete

echo "Done."
