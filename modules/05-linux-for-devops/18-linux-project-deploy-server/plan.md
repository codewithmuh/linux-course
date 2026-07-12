# Video 18 — Capstone: Deploy a Production Linux Server

**Module 5 · Linux for DevOps · Target length: ~30–40 min (project video)**

> **Cold-open hook (first 20s):** "One fresh cloud server. By the end of this video it's secured, serving a real app, backing itself up, and monitored — using everything from this course. Let's ship it."

## The project
Take a bare Ubuntu server from zero to production-shaped, using every skill in the course:
1. **Create users** — non-root `deploy` user with sudo (Module 2)
2. **Secure SSH** — key-only login, disable root + password auth (Module 3)
3. **Configure Nginx** — install, serve a site, reverse-proxy the app (Modules 2 + 3)
4. **Deploy a sample application** — run it as a systemd service (Module 2)
5. **Schedule backups** — the backup script on a cron timer (Modules 4 + 5)
6. **Monitor logs** — journald + the ops toolkit health checks (Modules 2 + 5)

This gives viewers a **real achievement at the end of the course** — a server they built and can put on a resume.

## Structure (project format)
- **Intro / architecture (3–5 min):** diagram the end state — user, firewall, SSH, Nginx → app, cron backups, monitoring.
- **Build it live (bulk of the video):** the six steps above, on camera, on a real cloud VM.
- **Prove it:** hit the app in a browser, kill the app service and watch systemd restart it, trigger a backup, show the health-check output.

## Build walkthrough (demo — full scripts go in this video's `demo/` folder)
```bash
# 1. user
sudo useradd -m -s /bin/bash deploy && sudo usermod -aG sudo deploy
# 2. SSH hardening (server)
ssh-copy-id deploy@<ip>
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
# 3. Nginx
sudo apt update && sudo apt install -y nginx
sudo systemctl enable --now nginx
# 4. app as a service
sudo tee /etc/systemd/system/sampleapp.service >/dev/null <<'EOF'
[Unit]
Description=Sample App
After=network.target
[Service]
User=deploy
ExecStart=/usr/bin/python3 /home/deploy/app/main.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload && sudo systemctl enable --now sampleapp
# 5. backups via cron
( crontab -l 2>/dev/null; echo "0 2 * * * /home/deploy/backup.sh" ) | crontab -
# 6. monitoring
journalctl -u sampleapp -f
./ops.sh disk && ./ops.sh ports
```

## 📝 Final challenge
- Reproduce the whole deploy on a fresh VM from scratch, then intentionally break the app service and confirm it self-heals, and confirm SSH now refuses password login.

## 📄 Cheat sheet (downloadable)
A one-page "production server checklist": user ✅ · SSH hardened ✅ · Nginx ✅ · app as service ✅ · backups scheduled ✅ · monitoring ✅.

## 🎯 Course wrap + next steps
- Recap the full journey: basics → admin → networking → scripting → real DevOps.
- **Next course in the roadmap:** Git & GitHub, then Docker. Point viewers to the devopsbymuh roadmap.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Deploy a Production Linux Server From Scratch (Full Project)
- **Primary keyword:** deploy linux server from scratch
- **Thumbnail idea:** "FROM SCRATCH → PRODUCTION" with a server + green checkmarks
- **Shorts to cut:** "Secure SSH in 3 steps" · "Run your app as a systemd service that self-heals" · the architecture-diagram walk
