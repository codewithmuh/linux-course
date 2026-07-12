# Video 16 — Linux in Real DevOps

**Module 5 · Linux for DevOps · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Here's what your Linux skills look like on the actual job — scheduling work, managing environments, and keeping disks from filling at 3am."

## What you'll learn
- Scheduled tasks with `cron` (and `crontab`)
- Environment variables (session, `~/.bashrc`, `/etc/environment`)
- Disk management: `df`, `du`, mounts, finding space hogs
- Compression + archives: `tar`, `gzip`, `zip`
- Lightweight monitoring habits

## 1. 🎨 Animated slides (3–5 min)
- The cron format (`* * * * *`) decoded field by field
- Where environment variables live and precedence
- `df` (filesystem level) vs `du` (directory level)

## 2. 💻 Hands-on demo (10–15 min)
```bash
# cron: run the health check every 15 min
crontab -e
# */15 * * * * /home/deploy/healthcheck.sh >> /var/log/health.log 2>&1
crontab -l

# environment variables
export APP_ENV=production
echo "$APP_ENV"
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc

# disk management
df -h
du -sh /var/* | sort -rh | head        # biggest dirs
du -h --max-depth=1 /var/log | sort -rh

# compression
tar -czf logs.tar.gz /var/log/myapp
tar -xzf logs.tar.gz -C /tmp/restore
gzip big.log && gunzip big.log.gz
```

## 3. 🏢 Real production example
Schedule the Module-4 scripts with cron, track down what filled `/var` with `du -sh | sort -rh`, and archive old logs — the daily maintenance loop of a real server.

## 4. 📝 Exercise / challenge
- Schedule your health-check via cron to log every 15 minutes, then use `du` to find the three largest directories under `/var` and archive one with `tar`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `crontab -e` / `-l` | Edit / list scheduled jobs |
| `*/15 * * * *` | Every 15 minutes |
| `df -h` | Free space per filesystem |
| `du -sh dir/* | sort -rh` | Biggest directories |
| `tar -czf a.tgz dir/` | Compress an archive |

## 6. 🎯 Next-lesson preview
→ **Video 17: Production Linux Tasks** — build the toolkit junior DevOps engineers use every single day.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux for DevOps in Practice (Cron, Env Vars, Disk, tar)
- **Primary keyword:** linux cron and disk management
- **Thumbnail idea:** A cron expression `*/15 * * * *` with a clock + disk gauge
- **Shorts to cut:** "Cron syntax finally explained" · "Find what's filling your disk with du"
