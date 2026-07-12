#!/usr/bin/env bash
# backup.sh — production-shaped Bash: functions, arrays, error handling, trap.
# Demonstrates the patterns that make a script safe to run unattended.
# Usage: ./backup.sh
set -euo pipefail

# A reusable logging function used throughout the script.
log() { echo "[$(date +%T)] $*"; }

# cleanup runs on EVERY exit — success, error, or Ctrl-C — thanks to the trap.
cleanup() { log "cleaning up temp files"; rm -f /tmp/backup.tmp; }
trap cleanup EXIT

# An array of the directories we want to back up.
targets=("/etc" "/var/www")

# A function that takes an argument and returns a meaningful exit code.
backup_one() {
  local src="$1"
  [[ -d "$src" ]] || { log "missing: $src"; return 1; }
  log "backing up $src"
}

# Loop over the array; keep going even if one target fails.
for t in "${targets[@]}"; do
  backup_one "$t" || log "WARN: failed on $t"
done

log "done (exit $?)"
