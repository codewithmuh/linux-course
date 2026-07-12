#!/usr/bin/env bash
set -euo pipefail

# setup-server.sh — take a fresh Ubuntu server from zero to production-ready.
#
# Run this ON the server, logged in as a user that can sudo (on a new cloud
# VM that is usually `ubuntu`). Read it before you run it: it hardens SSH
# and installs services.
#
# usage:  bash setup-server.sh
#
# Safety note: this script turns off SSH password login. Keep your current
# SSH session open, and test `ssh deploy@<server-ip>` from a second terminal
# BEFORE you log out.

# --- 1. Create a non-root deploy user with sudo (Module 2)
if ! id deploy &>/dev/null; then
  sudo useradd -m -s /bin/bash deploy
  sudo usermod -aG sudo deploy
fi

# --- 2. Give deploy your SSH key, then harden SSH (Modules 2 + 3)
# Copy the key you logged in with to the deploy user, so `ssh deploy@<ip>`
# works with the same key. chmod 700/600: SSH refuses keys anyone else can read.
sudo mkdir -p /home/deploy/.ssh
sudo cp ~/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys

# Key-only logins: no passwords, no root.
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# --- 3. Install Nginx and put it in front of the app (Modules 2 + 3)
sudo apt update && sudo apt install -y nginx
sudo systemctl enable --now nginx

# Reverse proxy: Nginx answers on port 80 and hands every request to the
# app listening on 127.0.0.1:8000.
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

# --- 4. Deploy the sample app as a systemd service (Module 2)
# The app is the smallest web server Python can make — enough to prove the
# whole chain (user -> Nginx -> app) works.
sudo mkdir -p /home/deploy/app
sudo tee /home/deploy/app/main.py >/dev/null <<'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler

class Hello(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from sampleapp - deployed on Linux!\n")

HTTPServer(("127.0.0.1", 8000), Hello).serve_forever()
EOF
sudo chown -R deploy:deploy /home/deploy/app

sudo cp "$(dirname "$0")/sampleapp.service" /etc/systemd/system/sampleapp.service
sudo systemctl daemon-reload
sudo systemctl enable --now sampleapp

# --- 5. Schedule a nightly backup at 02:00 (Modules 4 + 5)
# Module 4's backup script, minimal: archive /etc, keep the last 7.
# It goes in root's crontab so every file in /etc is readable.
sudo tee /home/deploy/backup.sh >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
mkdir -p /home/deploy/backups
tar -czf "/home/deploy/backups/etc_$(date +%F_%H%M).tar.gz" /etc
ls -1t /home/deploy/backups/etc_*.tar.gz | tail -n +8 | xargs -r rm --
EOF
sudo chmod +x /home/deploy/backup.sh
( sudo crontab -l 2>/dev/null || true; echo "0 2 * * * /home/deploy/backup.sh" ) | sudo crontab -

# --- 6. Verify everything came up (Modules 2 + 5)
echo
echo "=== The app, through Nginx ==="
curl -s http://127.0.0.1/ || echo "(app not answering yet)"
echo "=== Service states ==="
systemctl is-active nginx sampleapp || true
echo
echo "Done. Useful next commands:"
echo "  journalctl -u sampleapp -f      # follow the app's logs"
echo "  ssh deploy@<server-ip>          # test the deploy login BEFORE logging out"
