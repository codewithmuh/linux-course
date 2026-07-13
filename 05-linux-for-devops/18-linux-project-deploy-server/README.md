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
Work through the six steps on a fresh Ubuntu VM, logged in as a user that can `sudo` (on cloud VMs and Multipass that is usually `ubuntu`). The full runnable script is [`scripts/setup-server.sh`](scripts/setup-server.sh) — these are the key commands from it.

**No cloud account? Use a free local VM** — the whole capstone works on it:

```bash
multipass launch --name capstone      # create a fresh local Ubuntu VM
# give the VM your SSH key, so `ssh` behaves like on a real server:
multipass exec capstone -- sh -c 'cat >> .ssh/authorized_keys' < ~/.ssh/id_ed25519.pub
multipass shell capstone      # you are "on the server" — start step 1
multipass list                # this is your <ip> for the steps below
```

```bash
# 1. create a non-root deploy user with sudo
sudo useradd -m -s /bin/bash deploy && sudo usermod -aG sudo deploy   # create deploy + allow sudo

# 2. give deploy the SSH key you logged in with, then disable password + root login
#    (SSH refuses keys that other users can read — that is what the chmods are for)
sudo mkdir -p /home/deploy/.ssh                       # deploy's key folder
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys   # give deploy your key
sudo chown -R deploy:deploy /home/deploy/.ssh         # deploy owns it
sudo chmod 700 /home/deploy/.ssh && sudo chmod 600 /home/deploy/.ssh/authorized_keys  # strict, or SSH refuses
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config  # no passwords
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config                # no root login
sudo systemctl restart ssh                            # apply the SSH changes
# ⚠️ keep this session open — test `ssh deploy@<ip>` from a second terminal first

# 3. install Nginx and reverse-proxy port 80 to the app on 127.0.0.1:8000
sudo apt update && sudo apt install -y nginx          # install the web server
sudo systemctl enable --now nginx                     # start now + on every boot
sudo tee /etc/nginx/sites-available/sampleapp >/dev/null <<'EOF'
server {
    listen 80 default_server;              # answer on port 80
    location / {
        proxy_pass http://127.0.0.1:8000;  # hand every request to the app
        proxy_set_header Host $host;       # keep the original host name
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/sampleapp /etc/nginx/sites-enabled/sampleapp  # switch the site on
sudo rm -f /etc/nginx/sites-enabled/default           # remove the default welcome page
sudo nginx -t && sudo systemctl reload nginx          # -t = test the config first, then reload

# 4. deploy the app (a tiny Python web server) as a systemd service
#    setup-server.sh writes /home/deploy/app/main.py for you;
#    the unit file is scripts/sampleapp.service
sudo cp sampleapp.service /etc/systemd/system/sampleapp.service   # install the unit file
sudo systemctl daemon-reload && sudo systemctl enable --now sampleapp  # register + start the app

# 5. schedule nightly backups at 02:00 (root's crontab, so /etc is fully readable)
( sudo crontab -l 2>/dev/null || true; echo "0 2 * * * /home/deploy/backup.sh" ) | sudo crontab -   # keep old entries + add ours

# 6. monitor
journalctl -u sampleapp -f            # follow the app's logs live
systemctl is-active nginx sampleapp   # both must print: active
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
