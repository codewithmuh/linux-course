# Advanced Bash

> [Linux for DevOps](../../README.md) · Module 4 — Bash Scripting

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- Functions with arguments and return values
- Arrays
- Script arguments (`$1`, `$@`, `$#`) and option parsing
- Exit codes (`$?`) and what they mean
- Error handling with `set -euo pipefail` and `trap`

## Concepts

**Functions** are reusable building blocks — name a block of commands once and call it as many times as you like, passing arguments just like a script does.

Every command returns an **exit code**: `0` means success, anything non-zero means failure. `$?` holds the exit code of the last command, and a function can `return` its own.

`set -euo pipefail` is the safety belt that separates a laptop script from a production one:
- `-e` — exit immediately if any command fails
- `-u` — error on use of an unset variable (catches typos)
- `-o pipefail` — a pipeline fails if *any* stage fails, not just the last

**`trap`** runs cleanup code on exit — even when the script errors out or is interrupted — so temp files and locks never get left behind.

## Commands

```bash
# The full script lives in scripts/backup.sh — the key patterns:

log() { echo "[$(date +%T)] $*"; }          # a reusable function

cleanup() { rm -f /tmp/backup.tmp; }
trap cleanup EXIT                            # always runs on exit

targets=("/etc" "/var/www")                  # an array

backup_one() {                               # a function taking an argument
  local src="$1"
  [[ -d "$src" ]] || { echo "missing: $src"; return 1; }   # meaningful exit code
  echo "backing up $src"
}

for t in "${targets[@]}"; do                 # expand every array element
  backup_one "$t" || echo "WARN: failed on $t"
done
```

Run it and inspect the exit code:

```bash
chmod +x backup.sh
./backup.sh
echo "exit code: $?"
```

## In production
`set -euo pipefail` stops a script from blindly marching on after a failed step — the classic bug where a broken variable expands to nothing and the script deletes the wrong directory. `trap` guarantees cleanup runs even when the script errors out, so you never leak temp files or leave a lock behind.

## Practice
- Take the greeting script from the previous lesson and refactor it into functions. Add `set -euo pipefail`, validate the arguments, and return meaningful exit codes.

## Cheat sheet
| Syntax | Meaning |
|---|---|
| `f() { … }` | Define a function |
| `local x="$1"` | Function-scoped variable |
| `arr=(a b c)` / `"${arr[@]}"` | Array / expand all elements |
| `set -euo pipefail` | Fail fast and safely |
| `trap cleanup EXIT` | Run a function on exit |

## Scripts
- [`scripts/backup.sh`](scripts/backup.sh) — functions, an array, meaningful exit codes, `set -euo pipefail`, and `trap cleanup EXIT`.

---
← [Course home](../../README.md) · **Next:** [Automation Scripts](../15-automation-scripts/README.md)
