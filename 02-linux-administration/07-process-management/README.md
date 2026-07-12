# Process Management

> [Linux for DevOps](../../README.md) · Module 2 — Linux Administration

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- What a process is (PID, parent, state)
- Inspect processes: `ps`, `top`, `htop`
- Signals and stopping processes: `kill`, `kill -9`
- Job control: `jobs`, `bg`, `fg`, `&`, `Ctrl-Z`

## Concepts

A **process** is a running program. Each one has a **PID** (process ID) and a **parent PID** — every process is started by another, forming a tree. Processes move through states as they run, sleep, and eventually exit.

Any command you run can live in the **foreground** (tied to your terminal) or the **background** (running while you keep working). `&`, `Ctrl-Z`, `jobs`, `bg`, and `fg` move a job between the two.

You stop a process by sending it a **signal**. The two you'll use most:

| Signal | Number | Meaning |
|---|---|---|
| **SIGTERM** | 15 | Polite "please shut down" — lets the process clean up |
| **SIGKILL** | 9 | Forced kill — the process cannot ignore it, no cleanup |

Always try SIGTERM first; reach for `kill -9` only when a process refuses to stop.

## Commands
```bash
ps aux | head
ps aux | grep nginx
top            # q to quit; watch CPU/MEM
htop           # nicer, install: sudo apt install htop

# background / foreground
sleep 300 &
jobs
fg %1
# Ctrl-Z to suspend, then:
bg %1

# kill by PID and by name
kill <pid>          # SIGTERM
kill -9 <pid>       # SIGKILL (last resort)
pkill -f myscript
```

## In production
When a process goes out of control and eats 100% CPU, you find it in `top`, confirm it with `ps aux | grep`, and send it SIGTERM. Only if it will not stop do you escalate to SIGKILL. You will repeat this exact fix many times in real work.

## Practice
- Start a long-running `sleep` in the background, list your jobs, bring it to the foreground, suspend it, resume it in the background, then kill it by PID.

## Cheat sheet
| Command | What it does |
|---|---|
| `ps aux` | All processes |
| `top` / `htop` | Live resource monitor |
| `kill <pid>` | Ask a process to stop (15) |
| `kill -9 <pid>` | Force kill (9) |
| `cmd &` / `fg` / `bg` | Background / foreground jobs |

---
← [Course home](../../README.md) · **Next:** [Services & Logs](../08-services-and-logs/README.md)
