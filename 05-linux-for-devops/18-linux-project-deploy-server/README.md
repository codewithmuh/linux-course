# Capstone: Deploy a Production Linux Server

> [Linux for DevOps](../../README.md) · Module 5 — Linux for DevOps

> 📺 **Watch:** _video link coming soon_

This is the capstone. You take a bare Ubuntu server from zero to production-ready, using every skill in the course. At the end you have a secured, monitored, application-serving Linux server you built end to end — a real project you can put on a resume.

## The project
Six goals, each pulling on a skill from earlier modules:

1. **Create users** — a non-root `deploy` user with sudo. _(Module 2)_
2. **Secure SSH** — key-only login; disable root and password auth. _(Module 3)_
3. **Configure Nginx** — install, serve a site, and reverse-proxy the app. _(Modules 2 + 3)_
4. **Deploy a sample application** — run it as a systemd service so it survives reboots and crashes. _(Module 2)_
5. **Schedule backups** — the backup script on a cron timer. _(Modules 4 + 5)_
6. **Monitor logs** — journald plus the ops toolkit health checks. _(Modules 2 + 5)_

## Architecture
The end state: users reach the box only through a firewall and hardened SSH; Nginx fronts the app; cron backs it up nightly; journald and the ops toolkit keep watch.

```mermaid
flowchart LR
    user([User / Admin])
    user -->|HTTP / HTTPS| fw
    user -->|SSH · key only| fw
    subgraph server[Production server]
        fw[Firewall + hardened SSH]
        fw --> nginx[Nginx]
        nginx -->|reverse proxy| app[sampleapp<br/>systemd service]
        cron["cron · 0 2 * * *"] --> backup[backup.sh]
        backup --> store[(Nightly backups)]
        app -. logs .-> mon[journald + ops.sh]
    end
```

## Build it
Work through the six steps on a fresh cloud VM, logged in as a user that can `sudo` (on a new VM that is usually `ubuntu`). The full runnable script is [`scripts/setup-server.sh`](scripts/setup-server.sh) — these are the key commands from it:

```bash
# 1. create a non-root deploy user with sudo
sudo useradd -m -s /bin/bash deploy && sudo usermod -aG sudo deploy

# 2. give deploy the SSH key you logged in with, then disable password + root login
#    (SSH refuses keys that other users can read — that is what the chmods are for)
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh && sudo chmod 600 /home/deploy/.ssh/authorized_keys
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
# ⚠️ keep this session open — test `ssh deploy@<ip>` from a second terminal first

# 3. install Nginx and reverse-proxy port 80 to the app on 127.0.0.1:8000
sudo apt update && sudo apt install -y nginx
sudo systemctl enable --now nginx
sudo tee /etc/nginx/sites-available/sampleapp >/dev/null <<'EOF'
server {
    listen 80 default_server;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/sampleapp /etc/nginx/sites-enabled/sampleapp
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx

# 4. deploy the app (a tiny Python web server) as a systemd service
#    setup-server.sh writes /home/deploy/app/main.py for you;
#    the unit file is scripts/sampleapp.service
sudo cp sampleapp.service /etc/systemd/system/sampleapp.service
sudo systemctl daemon-reload && sudo systemctl enable --now sampleapp

# 5. schedule nightly backups at 02:00 (root's crontab, so /etc is fully readable)
( sudo crontab -l 2>/dev/null || true; echo "0 2 * * * /home/deploy/backup.sh" ) | sudo crontab -

# 6. monitor
journalctl -u sampleapp -f
systemctl is-active nginx sampleapp
```

## Prove it
Confirm the server actually behaves like a production box:

- **Serve traffic.** Open `http://<ip>` in a browser (or `curl http://<ip>`) and see the app respond through Nginx.
- **Log in as deploy.** From a second terminal: `ssh deploy@<ip>` — do this **before** closing your first session, so a mistake in SSH hardening cannot lock you out.
- **Self-heal.** Kill the app — `sudo systemctl kill sampleapp` — then run `systemctl status sampleapp` and watch systemd restart it automatically (that is `Restart=always` doing its job).
- **Back up on demand.** Run `/home/deploy/backup.sh` by hand and confirm a fresh archive lands where you expect, then check the cron entry with `crontab -l`.
- **Health check.** Run `./ops.sh disk` and `./ops.sh ports`, and tail the app's logs with `journalctl -u sampleapp -f`.

Everything on the checklist should now be true: user ✅ · SSH hardened ✅ · Nginx ✅ · app as a service ✅ · backups scheduled ✅ · monitoring ✅.

## Final challenge
- Reproduce the whole deploy on a fresh VM from scratch.
- Intentionally break the app service and confirm it self-heals.
- Confirm SSH now refuses password login (try `ssh -o PubkeyAuthentication=no deploy@<ip>` — it should be rejected).

## Scripts
- [`scripts/setup-server.sh`](scripts/setup-server.sh) — runs all six build steps end to end on a fresh Ubuntu server (read it first — it hardens SSH).
- [`scripts/sampleapp.service`](scripts/sampleapp.service) — the systemd unit that runs the sample app and restarts it on failure.

---
← [Course home](../../README.md) · 🎉 **You finished the course!** Next up on the channel: **Git & GitHub**.
