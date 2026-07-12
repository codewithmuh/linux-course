# Video 05 — Users & Groups

**Module 2 · Linux Administration · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "The #1 way servers get owned? Everyone running as root. Let's fix that — properly."

## What you'll learn
- The root user and `sudo` (why you almost never log in as root)
- Create and manage users: `useradd`, `passwd`
- Groups and identity: `groups`, `id`
- Where users and groups actually live (`/etc/passwd`, `/etc/group`, `/etc/sudoers`)

## 1. 🎨 Animated slides (3–5 min)
- Users, groups, and the root superuser
- Least-privilege: why `sudo` beats logging in as root
- Anatomy of an `/etc/passwd` line (uid, gid, home, shell)

## 2. 💻 Hands-on demo (10–15 min)
```bash
id
whoami
groups

# create a user + set password
sudo useradd -m -s /bin/bash deploy
sudo passwd deploy

# grant sudo (Debian/Ubuntu)
sudo usermod -aG sudo deploy

# inspect
id deploy
grep deploy /etc/passwd
getent group sudo

# run one command as another user
sudo -u deploy whoami
```

## 3. 🏢 Real production example
Standard server hardening: create a non-root `deploy` user, give it sudo, disable direct root SSH login. Apps and CI connect as `deploy`, never root.

## 4. 📝 Exercise / challenge
- Create a user `appuser`, add it to a new `webadmins` group, confirm with `id`, and run a command as that user with `sudo -u`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `id` / `whoami` | Your uid/gid / username |
| `useradd -m -s /bin/bash u` | Create user with home + shell |
| `usermod -aG group u` | Add user to a group |
| `passwd u` | Set a user's password |
| `sudo -u u cmd` | Run a command as user `u` |

## 6. 🎯 Next-lesson preview
→ **Video 06: Linux Permissions** — you know *who* the users are; now control *what* they can touch.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux Users, Groups & sudo (Stop Running as Root)
- **Primary keyword:** linux users and groups
- **Thumbnail idea:** root ❌ vs deploy ✅ with a shield
- **Shorts to cut:** "Never SSH as root — do this instead" · "What /etc/passwd actually stores"
