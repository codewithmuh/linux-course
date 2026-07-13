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
ps aux | head       # ps = "process status" — list running processes
ps aux | grep nginx # find nginx among all processes
top                 # top = "table of processes" — live view; q to quit
htop                # Hisham's top — nicer; install: sudo apt install htop

# background / foreground   (bg / fg = "background" / "foreground")
sleep 300 &         # & = run it in the background
jobs                # list this shell's background jobs
fg %1               # bring job 1 back to the front
# Ctrl-Z to suspend, then:
bg %1               # let job 1 continue in the background

# kill by PID ("process ID") and by name
kill <pid>          # SIGTERM = "signal: terminate" — polite
kill -9 <pid>       # SIGKILL = "signal: kill" — forced, last resort
pkill -f myscript   # pkill = "process kill" by name
```

## What the names mean

| Command | Stands for |
|---|---|
| `ps` | **p**rocess **s**tatus |
| `top` | **t**able **o**f **p**rocesses |
| `htop` | **H**isham's **top** — written by Hisham Muhammad |
| PID | **p**rocess **ID** |
| `bg` / `fg` | **b**ack**g**round / **f**ore**g**round |
| SIGTERM / SIGKILL | **sig**nal **term**inate / **sig**nal **kill** |

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
