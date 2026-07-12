# Linux in Real DevOps

> [Linux for DevOps](../../README.md) · Module 5 — Linux for DevOps

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- Schedule recurring work with `cron` (and `crontab`)
- Manage environment variables (session, `~/.bashrc`, `/etc/environment`)
- Track disk usage: `df`, `du`, mounts, and finding space hogs
- Compress and archive with `tar`, `gzip`, and `zip`
- Build lightweight monitoring habits

## Concepts
On a real server, most of your Linux skill turns into three recurring jobs: running work on a schedule, controlling the environment your programs see, and keeping disks from filling up.

**Cron** runs commands on a schedule. A cron line has five time fields followed by the command:

```
* * * * *  command
│ │ │ │ │
│ │ │ │ └─ day of week (0–6, Sun=0)
│ │ │ └─── month (1–12)
│ │ └───── day of month (1–31)
│ └─────── hour (0–23)
└───────── minute (0–59)
```

So `*/15 * * * *` means "every 15 minutes." Each `*` is a wildcard meaning "every value."

**Environment variables** live at a few levels, and later ones override earlier ones for a given shell:
- Set for one session with `export VAR=value` — gone when you close the shell.
- Put in `~/.bashrc` to load for your user in every new interactive shell.
- Put in `/etc/environment` to set system-wide values for all users.

**Disk tools** answer two different questions. `df` works at the **filesystem** level — how full each mounted disk is. `du` works at the **directory** level — which folders are eating the space. You reach for `df` first ("which disk is full?") and `du` second ("what inside it is the problem?").

## Commands
```bash
# cron: run the health check every 15 minutes
crontab -e
# add this line, then save:
# */15 * * * * /home/deploy/healthcheck.sh >> /var/log/health.log 2>&1
crontab -l                              # list your scheduled jobs

# environment variables
export APP_ENV=production               # set for this session
echo "$APP_ENV"                         # read it back
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc   # make it persist

# disk management
df -h                                   # free space per filesystem
du -sh /var/* | sort -rh | head         # biggest directories under /var
du -h --max-depth=1 /var/log | sort -rh # drill into one directory

# compression + archives
tar -czf logs.tar.gz /var/log/myapp     # create a gzipped archive
tar -xzf logs.tar.gz -C /tmp/restore    # extract it somewhere
gzip big.log && gunzip big.log.gz       # compress / decompress a single file
```

## In production
You schedule your Module 4 scripts with cron so the health check runs on its own every 15 minutes. When a disk alert fires, you track down what filled `/var` with `du -sh /var/* | sort -rh`, then archive the old logs with `tar` to reclaim the space. That measure-then-clean loop is the everyday maintenance of a real server.

## Practice
- Schedule your health-check script with cron so it logs every 15 minutes.
- Use `du` to find the three largest directories under `/var`.
- Archive one of them with `tar` and confirm the archive extracts cleanly.

## Cheat sheet
| Command | What it does |
|---|---|
| `crontab -e` / `-l` | Edit / list scheduled jobs |
| `*/15 * * * *` | Every 15 minutes |
| `df -h` | Free space per filesystem |
| `du -sh dir/* \| sort -rh` | Biggest directories |
| `tar -czf a.tgz dir/` | Compress an archive |

---
← [Course home](../../README.md) · **Next:** [Production Linux Tasks](../17-production-linux-tasks/README.md)
