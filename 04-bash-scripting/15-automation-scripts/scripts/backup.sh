#!/usr/bin/env bash
# backup.sh — create a timestamped tarball of a directory, then keep only the
# most recent N archives (rotation).
# Usage: ./backup.sh [source-dir] [backup-dir]
set -euo pipefail

# --- config (override via arguments) ---
SRC="${1:-/etc}"          # what to back up
DEST="${2:-/backups}"     # where archives are stored
KEEP=7                    # how many archives to retain

name="$(basename "$SRC")"
ts="$(date +%F_%H%M)"
archive="$DEST/${name}_${ts}.tar.gz"

mkdir -p "$DEST"

echo "Backing up $SRC -> $archive"
tar -czf "$archive" "$SRC"

# Rotation: newest-first, skip the KEEP we want to keep, delete the rest.
echo "Pruning old backups (keeping last $KEEP)"
ls -1t "$DEST/${name}_"*.tar.gz | tail -n +$((KEEP + 1)) | xargs -r rm --

echo "Done."
