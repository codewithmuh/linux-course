# Video 08 — Services & Logs

**Module 2 · Linux Administration · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Your app needs to start on boot, restart if it crashes, and log everything. That's systemd — and it's easier than you think."

## What you'll learn
- What systemd is and what a service (unit) is
- Manage services: `systemctl` (start/stop/restart/enable/status)
- Read logs the modern way: `journalctl`
- Legacy `service` command and traditional log files in `/var/log`

## 1. 🎨 Animated slides (3–5 min)
- init → systemd: who starts everything
- A unit file's anatomy (`[Unit] [Service] [Install]`)
- `enable` (on boot) vs `start` (now) — the distinction beginners miss

## 2. 💻 Hands-on demo (10–15 min)
```bash
systemctl status nginx
sudo systemctl start nginx
sudo systemctl enable nginx        # start on boot
sudo systemctl restart nginx
systemctl is-active nginx
systemctl list-units --type=service

# logs
journalctl -u nginx --no-pager | tail
journalctl -u nginx -f             # follow live
journalctl --since "10 min ago"
tail -f /var/log/nginx/error.log

# write a tiny custom service
sudo nano /etc/systemd/system/hello.service
sudo systemctl daemon-reload
sudo systemctl enable --now hello.service
```

## 3. 🏢 Real production example
Run a Python/Node app as a managed service so it survives crashes and reboots, then tail its logs with `journalctl -u myapp -f` during a deploy.

## 4. 📝 Exercise / challenge
- Write a minimal `hello.service` that runs a script, enable it, confirm it starts on boot, and read its output via `journalctl -u hello`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `systemctl status svc` | Is it running + recent logs |
| `systemctl enable --now svc` | Start now + on boot |
| `systemctl restart svc` | Restart |
| `journalctl -u svc -f` | Follow a service's logs |
| `journalctl --since "1h ago"` | Time-filtered logs |

## 6. 🎯 Next-lesson preview
→ **Video 09: Package Management** — services come from packages. Let's install, update, and manage software the right way.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** systemd & Logs Explained (systemctl, journalctl)
- **Primary keyword:** systemctl journalctl tutorial
- **Thumbnail idea:** `● active (running)` in green + a log stream
- **Shorts to cut:** "Run any app as a systemd service" · "enable vs start — the difference"
