# Production Linux Tasks

> [Linux for DevOps](../../README.md) · Module 5 — Linux for DevOps

> 📺 **Watch:** _video link coming soon_

## What you'll learn
Build a small **ops toolkit** — one script with subcommands — that can:
- Check CPU
- Check RAM
- Check disk
- Restart services
- Analyze logs
- Monitor ports

This is the day-to-day work of a junior DevOps engineer, in one place you can reuse.

## Concepts
When something breaks, the mindset is always the same: **measure → locate → act**. You take readings (CPU, RAM, disk), narrow down where the problem lives (logs, ports), and only then change something.

The upgrade in this lesson is turning those ad-hoc commands into a **subcommand-style toolkit**. Instead of remembering six different commands, you wrap them in a single script and call `ops.sh cpu`, `ops.sh disk`, and so on. It reads like a menu and it lives in version control.

One habit worth building early: separate **read-only checks** from **actions that change state**. `cpu`, `ram`, `disk`, `logs`, and `ports` only look — they are safe to run anytime. `restart` actually changes the system, so it needs `sudo` and a confirmation that the service came back up. Keeping that line clear stops a "quick check" from turning into an outage.

## Commands
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

# run each subcommand
./ops.sh cpu            # read-only: safe to run anytime
./ops.sh disk           # read-only: safe to run anytime
./ops.sh logs nginx     # read-only: safe to run anytime
./ops.sh ports          # read-only: safe to run anytime
./ops.sh restart nginx  # changes the system — the only one that does
```

The full, hardened version of this script lives in [`scripts/ops.sh`](scripts/ops.sh).

## In production
A ticket comes in: "site is slow." You walk it with the toolkit — `ops.sh cpu` to check load, `ops.sh ram` for memory pressure, `ops.sh disk` in case something filled up, `ops.sh logs nginx` for errors, and `ops.sh ports` to confirm the service is actually listening. Each step narrows the problem down. This is the job.

## Practice
- Extend the toolkit with a `top-ip` subcommand that reports the top 10 client IPs from an Nginx access log (reuse the `awk` one-liner from Module 1's networking lesson).
- Run the full triage sequence (`cpu`, `ram`, `disk`, `logs`, `ports`) against a service on your machine and note what each reading tells you.

## Cheat sheet
| Check | Command |
|---|---|
| CPU | `top -bn1 \| grep Cpu` |
| RAM | `free -h` |
| Disk | `df -h` + `du -sh /var/* \| sort -rh` |
| Restart svc | `systemctl restart <svc>` |
| Logs | `journalctl -u <svc> -f` |
| Ports | `ss -tulpn` |

## Scripts
- [`scripts/ops.sh`](scripts/ops.sh) — the CPU/RAM/disk/restart/logs/ports ops toolkit as a runnable subcommand script.

---
← [Course home](../../README.md) · **Next:** [Capstone: Deploy a Production Server](../18-linux-project-deploy-server/README.md)
