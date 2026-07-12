# Video 07 — Process Management

**Module 2 · Linux Administration · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "The server's at 100% CPU. Something's eating it alive. In two minutes you'll find it and kill it."

## What you'll learn
- What a process is (PID, parent, state)
- Inspect processes: `ps`, `top`, `htop`
- Signals and stopping processes: `kill`, `kill -9`
- Job control: `jobs`, `bg`, `fg`, `&`, `Ctrl-Z`

## 1. 🎨 Animated slides (3–5 min)
- Process lifecycle and PIDs / parent PIDs
- Foreground vs background jobs
- Signals: SIGTERM (15, polite) vs SIGKILL (9, forced)

## 2. 💻 Hands-on demo (10–15 min)
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

## 3. 🏢 Real production example
A runaway process pins CPU: find it in `top`, confirm with `ps aux | grep`, send SIGTERM, escalate to SIGKILL only if it won't stop. Classic on-call move.

## 4. 📝 Exercise / challenge
- Start a long-running `sleep` in the background, list jobs, bring it to the foreground, suspend it, resume it in the background, then kill it by PID.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `ps aux` | All processes |
| `top` / `htop` | Live resource monitor |
| `kill <pid>` | Ask a process to stop (15) |
| `kill -9 <pid>` | Force kill (9) |
| `cmd &` / `fg` / `bg` | Background / foreground jobs |

## 6. 🎯 Next-lesson preview
→ **Video 08: Services & Logs** — most processes you care about are *services*. Let's manage them the right way with systemd.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux Process Management (top, kill, jobs) for DevOps
- **Primary keyword:** linux process management
- **Thumbnail idea:** `top` at 100% CPU with a red process highlighted
- **Shorts to cut:** "Find what's eating your CPU" · "kill vs kill -9 — when to use which"
