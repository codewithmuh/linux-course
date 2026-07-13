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
# generate a key pair   (ssh-keygen = "SSH key generator"; -C adds a label)
ssh-keygen -t ed25519 -C "you@your-laptop"   # creates id_ed25519 (private) + id_ed25519.pub (public)

# copy the public key to a server
ssh-copy-id deploy@<server-ip>   # adds your public key to the server's authorized_keys
# now log in with no password
ssh deploy@<server-ip>           # the server checks your private key — no password asked

# ~/.ssh/config shortcut
# Host = the short name you type · HostName = the real IP
# User = who to log in as     · IdentityFile = which private key to use
cat >> ~/.ssh/config <<'EOF'
Host prod
  HostName 203.0.113.10
  User deploy
  IdentityFile ~/.ssh/id_ed25519
EOF
ssh prod            # that's it

# transfer files   (scp = "secure copy", sftp = "SSH File Transfer Protocol")
scp ./app.tar.gz prod:/tmp/            # upload: my machine → server's /tmp
scp prod:/var/log/nginx/error.log ./   # download: server → my current folder
sftp prod           # interactive session: put = upload, get = download

# hardening (server side): disable password + root login in /etc/ssh/sshd_config
```

## What the names mean

| Command | Stands for |
|---|---|
| `ssh` | **S**ecure **Sh**ell |
| `scp` | **s**ecure **c**o**p**y |
| `sftp` | **S**SH **F**ile **T**ransfer **P**rotocol |
| `ssh-keygen` | SSH **key gen**erator |
| `ed25519` | the name of the math curve the key uses — just pick it, it is the modern default |

## In production
You set up passwordless key-based access to a production box, add a `~/.ssh/config` alias so `ssh prod` just works, and `scp` a build artifact up for deployment.

## Practice
- Generate an ed25519 key.
- Install it on a server with `ssh-copy-id`.
- Add a `~/.ssh/config` host alias.
- `scp` a file in both directions.

**No cloud server?** Practice against your local Multipass VM. `ssh-copy-id` needs password login (Multipass disables it), so add your key like this instead, then connect to the IP shown by `multipass list`:

```bash
multipass exec devops -- sh -c 'cat >> .ssh/authorized_keys' < ~/.ssh/id_ed25519.pub
multipass list                        # note the VM's IP
ssh ubuntu@<vm-ip>                    # a real SSH login, fully local
```

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
