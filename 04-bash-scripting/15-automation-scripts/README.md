# Automation Scripts

> [Linux for DevOps](../../README.md) · Module 4 — Bash Scripting

> 📺 **Watch:** _video link coming soon_

## What you'll learn
Build four real, reusable scripts every server should have:
- **Backup** — archive a directory into a timestamped tarball, with rotation
- **Health check** — test CPU / RAM / disk against thresholds, exit non-zero on breach
- **Log cleanup** — compress old logs and delete the really old ones
- **Monitoring** — a periodic one-line snapshot you can schedule with cron

## Concepts

A good ops script follows the same shape every time:
- **Config at the top** — thresholds, paths, and retention counts in named variables, so you tune behaviour in one place.
- **Functions and logging** — small named steps and a consistent log line keep output readable and reusable.
- **Exit codes** — return non-zero when something is wrong so a scheduler (or another script) can react to it.

Aim for **idempotency and safe defaults**: running a script twice should not cause damage, and good defaults mean it does the right thing with no arguments. In the next module these same scripts get scheduled with **cron** so they run with nobody watching.

## Commands

Each snippet below is the core idea; the full, hardened versions live in [`scripts/`](scripts/).

```bash
# backup.sh — timestamped tarball, then keep only the last 7
ts=$(date +%F_%H%M)                              # timestamp like 2026-07-13_0230
tar -czf "/backups/etc_$ts.tar.gz" /etc          # archive /etc into one dated file
ls -1t /backups/etc_*.tar.gz | tail -n +8 | xargs -r rm --   # newest first, delete from #8 on

# healthcheck.sh — compare against thresholds
disk=$(df / | awk 'END{print $5}' | tr -d '%')   # % used on the root disk (number only)
mem=$(free | awk '/Mem:/{printf "%.0f", $3/$2*100}')   # memory used, as a %
[[ $disk -gt 80 ]] && echo "WARN disk ${disk}%"  # warn above 80%
[[ $mem  -gt 90 ]] && echo "WARN mem ${mem}%"    # warn above 90%

# logclean.sh — compress logs older than 7 days, delete older than 30
find /var/log/myapp -name "*.log" -mtime +7  -exec gzip {} \;   # -mtime +7 = older than 7 days
find /var/log/myapp -name "*.gz"  -mtime +30 -delete            # remove ancient archives

# monitor.sh — one-line snapshot, ideal for cron
echo "$(date +%F_%T) load=$(uptime | awk -F'load average:' '{print $2}')"   # date + CPU load
```

## In production
These are the exact kinds of scripts teams schedule with cron to keep servers healthy without anyone watching them. A backup runs nightly and rotates itself, a health check gates an alert on its exit code, log cleanup keeps disks from filling, and a monitor line lands in a log you can grep later. This toolkit gets expanded once you start scheduling in the next module.

## Practice
- Harden the health check: make the thresholds configurable via arguments (or environment variables), and exit `1` when any threshold is breached so it can gate a cron alert.

## Cheat sheet
| Task | Key command |
|---|---|
| Timestamped archive | `tar -czf name_$(date +%F).tar.gz dir/` |
| Disk % used | `df / \| awk 'END{print $5}'` |
| Mem % used | `free \| awk '/Mem:/{...}'` |
| Delete old files | `find dir -mtime +N -delete` |

## Scripts
- [`scripts/backup.sh`](scripts/backup.sh) — timestamped tarball of a directory, keeping only the last 7.
- [`scripts/healthcheck.sh`](scripts/healthcheck.sh) — CPU / RAM / disk thresholds; exits non-zero on any breach.
- [`scripts/logclean.sh`](scripts/logclean.sh) — gzip logs older than 7 days, delete archives older than 30.
- [`scripts/monitor.sh`](scripts/monitor.sh) — one-line load / memory / disk snapshot for cron.

---
← [Course home](../../README.md) · **Next:** [Linux in Real DevOps](../../05-linux-for-devops/16-linux-in-real-devops/README.md)
