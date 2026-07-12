#!/usr/bin/env bash
set -euo pipefail

# setup-server.sh — take a bare Ubuntu server from zero to production-shaped.
# Best-effort capture of the capstone's six build steps. Read it before you
# run it: it hardens SSH and installs services. Run as a sudo-capable user.
#
# usage: ./setup-server.sh <server-ip>

SERVER_IP="${1:?usage: $0 <server-ip>}"

# 1. Create a non-root deploy user with sudo (Module 2)
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG sudo deploy

# 2. Harden SSH: install your key, then disable password + root login (Module 3)
ssh-copy-id "deploy@${SERVER_IP}"
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart ssh

# 3. Install and enable Nginx to serve the site / reverse-proxy the app (Modules 2 + 3)
sudo apt update && sudo apt install -y nginx
sudo systemctl enable --now nginx

# 4. Run the sample app as a systemd service so it survives reboots + crashes (Module 2)
#    The unit lives alongside this script — see sampleapp.service.
sudo cp "$(dirname "$0")/sampleapp.service" /etc/systemd/system/sampleapp.service
sudo systemctl daemon-reload
sudo systemctl enable --now sampleapp

# 5. Schedule the backup script nightly at 02:00 via cron (Modules 4 + 5)
( crontab -l 2>/dev/null; echo "0 2 * * * /home/deploy/backup.sh" ) | crontab -

# 6. Monitor: follow the app's journald logs and run the ops toolkit checks (Modules 2 + 5)
journalctl -u sampleapp -f &
./ops.sh disk && ./ops.sh ports
