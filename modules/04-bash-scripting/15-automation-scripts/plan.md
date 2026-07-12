# Video 15 — Automation Scripts

**Module 4 · Bash Scripting · Target length: ~20–22 min**

> **Cold-open hook (first 20s):** "Four scripts every server should have. We'll build all four — backup, health check, log cleanup, and monitoring — and they're yours to keep."

## What you'll learn
Build four real, reusable scripts (drop the finished versions in this video's `demo/` folder):
- **Backup script** — archive dirs, timestamped, with rotation
- **Health check** — CPU / RAM / disk thresholds, exit non-zero on breach
- **Log cleanup** — delete/compress logs older than N days
- **Server monitoring** — periodic snapshot, alert when a threshold trips

## 1. 🎨 Animated slides (3–5 min)
- Anatomy of a good ops script (config at top, functions, logging, exit codes)
- Idempotency and safe defaults
- How these hook into cron (teased for Module 5)

## 2. 💻 Hands-on demo (10–15 min)
```bash
# backup.sh — timestamped tarball + keep last 7
ts=$(date +%F_%H%M)
tar -czf "/backups/etc_$ts.tar.gz" /etc
ls -1t /backups/etc_*.tar.gz | tail -n +8 | xargs -r rm --

# healthcheck.sh — thresholds
disk=$(df / | awk 'END{print $5}' | tr -d '%')
mem=$(free | awk '/Mem:/{printf "%.0f", $3/$2*100}')
[[ $disk -gt 80 ]] && echo "WARN disk ${disk}%"
[[ $mem  -gt 90 ]] && echo "WARN mem ${mem}%"

# logclean.sh — compress logs older than 7 days, delete older than 30
find /var/log/myapp -name "*.log" -mtime +7  -exec gzip {} \;
find /var/log/myapp -name "*.gz"  -mtime +30 -delete

# monitor.sh — one-line snapshot for cron
echo "$(date +%F_%T) load=$(uptime | awk -F'load average:' '{print $2}')"
```

## 3. 🏢 Real production example
These are the exact scripts teams schedule with cron to keep boxes healthy without anyone watching. This video's outputs become the toolkit expanded in video 17.

## 4. 📝 Exercise / challenge
- Harden the health-check: make thresholds configurable via arguments, and exit `1` when any threshold is breached so it can gate a cron alert.

## 5. 📄 Cheat sheet (downloadable)
| Task | Key command |
|---|---|
| Timestamped archive | `tar -czf name_$(date +%F).tar.gz dir/` |
| Disk % used | `df / | awk 'END{print $5}'` |
| Mem % used | `free | awk '/Mem:/{...}'` |
| Delete old files | `find dir -mtime +N -delete` |

## 6. 🎯 Next-lesson preview
→ **Video 16: Linux in Real DevOps** — Module 5 begins. Schedule these scripts, manage env + disk, and think like an operator.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** 4 Bash Scripts Every Server Needs (Backup, Health, Cleanup, Monitor)
- **Primary keyword:** bash automation scripts
- **Thumbnail idea:** 4 script icons in a 2×2 grid, "yours to keep"
- **Shorts to cut:** "A backup script with rotation in 5 lines" · "Disk-usage health check one-liner"
