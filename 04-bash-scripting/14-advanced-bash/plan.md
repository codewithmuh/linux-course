# Video 14 — Advanced Bash

**Module 4 · Bash Scripting · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "The difference between a script that works on your laptop and one you'd run in production? Error handling. Let's write the production kind."

## What you'll learn
- Functions (with arguments and return values)
- Arrays
- Script arguments (`$1`, `$@`, `$#`) and option parsing
- Exit codes (`$?`) and what they mean
- Error handling: `set -euo pipefail`, `trap`

## 1. 🎨 Animated slides (3–5 min)
- Functions as reusable building blocks
- Exit codes: 0 = success, non-zero = failure
- `set -euo pipefail` — the safety belt, line by line
- `trap` for cleanup on exit/error

## 2. 💻 Hands-on demo (10–15 min)
```bash
cat > backup.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

log() { echo "[$(date +%T)] $*"; }

cleanup() { log "cleaning up temp files"; rm -f /tmp/backup.tmp; }
trap cleanup EXIT

targets=("/etc" "/var/www")   # array

backup_one() {
  local src="$1"
  [[ -d "$src" ]] || { log "missing: $src"; return 1; }
  log "backing up $src"
}

for t in "${targets[@]}"; do
  backup_one "$t" || log "WARN: failed on $t"
done

log "done (exit $?)"
EOF

chmod +x backup.sh
./backup.sh
echo "exit code: $?"
```

## 3. 🏢 Real production example
Why `set -euo pipefail` prevents a script from silently continuing after a failed step (the bug that deletes the wrong directory), and how `trap` guarantees cleanup even when a script errors out.

## 4. 📝 Exercise / challenge
- Refactor video 13's script into functions, add `set -euo pipefail`, validate arguments, and return meaningful exit codes.

## 5. 📄 Cheat sheet (downloadable)
| Syntax | Meaning |
|---|---|
| `f() { … }` | Define a function |
| `local x="$1"` | Function-scoped variable |
| `arr=(a b c)` / `"${arr[@]}"` | Array / expand all |
| `set -euo pipefail` | Fail fast + safely |
| `trap cleanup EXIT` | Run on exit |

## 6. 🎯 Next-lesson preview
→ **Video 15: Automation Scripts** — put it all together into real scripts: backups, health checks, log cleanup, monitoring.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Advanced Bash (Functions, Error Handling, set -euo pipefail)
- **Primary keyword:** bash error handling set -e
- **Thumbnail idea:** `set -euo pipefail` glowing with a "production-safe" stamp
- **Shorts to cut:** "The one line that makes Bash safe" · "trap: cleanup that always runs"
