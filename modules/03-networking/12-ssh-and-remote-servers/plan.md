# Video 12 — SSH & Remote Servers

**Module 3 · Networking · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "You'll spend your whole career inside SSH. Let's make you fast, secure, and password-free."

## What you'll learn
- How SSH works (public/private key crypto, at a glance)
- Generate and use SSH keys (`ssh-keygen`, `ssh-copy-id`)
- Passwordless login + the `~/.ssh/config` shortcut
- Move files: `scp` and `sftp`
- Basic SSH hardening

## 1. 🎨 Animated slides (3–5 min)
- Public vs private key — which goes where
- The handshake: why you never send your private key
- `authorized_keys` and `known_hosts`

## 2. 💻 Hands-on demo (10–15 min)
```bash
# generate a key pair
ssh-keygen -t ed25519 -C "deploy@devopsbymuh"

# copy the public key to a server
ssh-copy-id deploy@<server-ip>
# now log in with no password
ssh deploy@<server-ip>

# ~/.ssh/config shortcut
cat >> ~/.ssh/config <<'EOF'
Host prod
  HostName 203.0.113.10
  User deploy
  IdentityFile ~/.ssh/id_ed25519
EOF
ssh prod            # that's it

# transfer files
scp ./app.tar.gz prod:/tmp/
scp prod:/var/log/nginx/error.log ./
sftp prod           # interactive: put / get

# hardening (server side): disable password + root login in /etc/ssh/sshd_config
```

## 3. 🏢 Real production example
Set up passwordless key-based access to a production box, add a `~/.ssh/config` alias so `ssh prod` just works, and `scp` a build artifact up for deployment.

## 4. 📝 Exercise / challenge
- Generate an ed25519 key, install it on a server with `ssh-copy-id`, add a `~/.ssh/config` host alias, and `scp` a file both directions.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `ssh-keygen -t ed25519` | Make a key pair |
| `ssh-copy-id user@host` | Install your public key |
| `ssh alias` (via config) | One-word login |
| `scp src host:dest` | Copy files over SSH |
| `sftp host` | Interactive file transfer |

## 6. 🎯 Next-lesson preview
→ **Video 13: Bash Basics** — Module 4 begins. Stop typing the same commands twice — automate them.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** SSH Explained (Keys, Config, scp) — DevOps Essentials
- **Primary keyword:** ssh keys tutorial
- **Thumbnail idea:** A key icon + "passwordless login" + terminal `ssh prod`
- **Shorts to cut:** "Passwordless SSH in 3 commands" · "The ~/.ssh/config trick nobody teaches"
