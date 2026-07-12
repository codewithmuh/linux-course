# Video 17 — Production Linux Tasks

**Module 5 · Linux for DevOps · Target length: ~20–22 min**

> **Cold-open hook (first 20s):** "This is the actual day-to-day of a junior DevOps engineer. We're going to build the exact toolkit they reach for — and you'll have it by the end."

## What you'll learn
Build a small **ops toolkit** (finished scripts go in this video's `demo/` folder) that can:
- Check CPU
- Check RAM
- Check disk
- Restart services
- Analyze logs
- Monitor ports

**This is what junior DevOps engineers actually do.**

## 1. 🎨 Animated slides (3–5 min)
- The triage mindset: measure → locate → act
- Turning ad-hoc commands into a reusable, subcommand-style toolkit
- Read-only checks vs actions that change state (and guarding the latter)

## 2. 💻 Hands-on demo (10–15 min)
```bash
# ops.sh — a single toolkit with subcommands
#   usage: ./ops.sh cpu|ram|disk|restart <svc>|logs <svc>|ports
case "$1" in
  cpu)   top -bn1 | grep "Cpu(s)";;
  ram)   free -h;;
  disk)  df -h; echo; du -sh /var/* 2>/dev/null | sort -rh | head;;
  restart) sudo systemctl restart "$2" && systemctl is-active "$2";;
  logs)  journalctl -u "$2" --since "1 hour ago" --no-pager | tail -n 50;;
  ports) ss -tulpn;;
  *) echo "usage: $0 cpu|ram|disk|restart <svc>|logs <svc>|ports"; exit 1;;
esac
```
Run each subcommand live: `./ops.sh cpu`, `./ops.sh disk`, `./ops.sh logs nginx`, `./ops.sh ports`, `./ops.sh restart nginx`.

## 3. 🏢 Real production example
A ticket comes in: "site is slow." Walk it with the toolkit — `ops.sh cpu`, `ops.sh ram`, `ops.sh disk`, `ops.sh logs nginx`, `ops.sh ports` — and narrate the reasoning at each step. This *is* the job.

## 4. 📝 Exercise / challenge
- Extend the toolkit with a `top-ip` subcommand that reports the top 10 client IPs from an Nginx access log (reuse the awk one-liner from video 04).

## 5. 📄 Cheat sheet (downloadable)
| Check | Command |
|---|---|
| CPU | `top -bn1 | grep Cpu` |
| RAM | `free -h` |
| Disk | `df -h` + `du -sh /var/* | sort -rh` |
| Restart svc | `systemctl restart <svc>` |
| Logs | `journalctl -u <svc> -f` |
| Ports | `ss -tulpn` |

## 6. 🎯 Next-lesson preview
→ **Video 18: The Capstone** — put every skill together and deploy a real, production Linux server.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** A Day as a Junior DevOps Engineer (The Real Toolkit)
- **Primary keyword:** junior devops engineer tasks
- **Thumbnail idea:** A terminal "toolkit" menu (cpu/ram/disk/logs/ports)
- **Shorts to cut:** "The 6 checks every DevOps engineer runs" · "Build an ops toolkit in one script"
