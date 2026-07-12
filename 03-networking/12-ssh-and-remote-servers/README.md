# SSH & Remote Servers

> [Linux for DevOps](../../README.md) · Module 3 — Networking

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- How SSH works (public/private key crypto, at a glance)
- Generate and use SSH keys (`ssh-keygen`, `ssh-copy-id`)
- Passwordless login + the `~/.ssh/config` shortcut
- Move files: `scp` and `sftp`
- Basic SSH hardening

## Concepts
SSH secures a connection with a **key pair**: a **private key** that never leaves your machine and a **public key** you hand out freely. The trick is which goes where — you copy your *public* key onto the server, and it stays in `authorized_keys`. During the handshake the server proves you hold the matching private key without you ever sending it, which is why key-based login is both password-free and safer than a password.

The first time you connect, the server's identity is recorded in your `known_hosts` so you're warned if it ever changes.

## Commands
```bash
# generate a key pair (-C adds a label so you know whose key this is)
ssh-keygen -t ed25519 -C "you@your-laptop"

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

## In production
You set up passwordless key-based access to a production box, add a `~/.ssh/config` alias so `ssh prod` just works, and `scp` a build artifact up for deployment.

## Practice
- Generate an ed25519 key.
- Install it on a server with `ssh-copy-id`.
- Add a `~/.ssh/config` host alias.
- `scp` a file in both directions.

## Cheat sheet
| Command | What it does |
|---|---|
| `ssh-keygen -t ed25519` | Make a key pair |
| `ssh-copy-id user@host` | Install your public key |
| `ssh alias` (via config) | One-word login |
| `scp src host:dest` | Copy files over SSH |
| `sftp host` | Interactive file transfer |

---
← [Course home](../../README.md) · **Next:** [Bash Basics](../../04-bash-scripting/13-bash-basics/README.md)
