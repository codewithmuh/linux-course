# Video 09 — Package Management

**Module 2 · Linux Administration · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Every tool you'll ever use starts with one command. Let's master installing software on both Debian and Red Hat systems."

## What you'll learn
- Debian/Ubuntu family: `apt`, `dpkg`
- Red Hat family: `yum`, `dnf`
- Repositories, updates, and why `apt update` before `apt upgrade`
- Searching, inspecting, and removing packages

## 1. 🎨 Animated slides (3–5 min)
- What a package + package manager is (vs downloading binaries)
- Repositories and the metadata index
- The two big families: `.deb` (apt/dpkg) vs `.rpm` (yum/dnf)

## 2. 💻 Hands-on demo (10–15 min)
```bash
# Debian / Ubuntu
sudo apt update
sudo apt upgrade -y
sudo apt install -y htop tree jq
apt search nginx
apt show nginx
dpkg -l | grep nginx
sudo apt remove --purge htop

# Red Hat / Fedora / Amazon Linux
sudo dnf update -y
sudo dnf install -y htop
sudo yum install -y git          # older systems
rpm -qa | grep git
```

## 3. 🏢 Real production example
The first lines of nearly every server bootstrap / Dockerfile / Ansible playbook: `apt update && apt install ...`. Show how a base image gets the tools it needs.

## 4. 📝 Exercise / challenge
- Update your system, install `tree` and `jq`, inspect one with `apt show`, then cleanly remove it with `--purge`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `apt update` | Refresh package index |
| `apt install -y pkg` | Install |
| `apt remove --purge pkg` | Remove + config |
| `dpkg -l` / `rpm -qa` | List installed packages |
| `dnf install -y pkg` | Install (RHEL/Fedora) |

## 6. 🎯 Next-lesson preview
→ **Video 10: Linux Networking** — Module 3 begins. Let's connect your server to the world.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux Package Management (apt, dnf, yum) Explained
- **Primary keyword:** apt vs yum package management
- **Thumbnail idea:** Debian + Red Hat logos, `apt install` prompt
- **Shorts to cut:** "apt update vs upgrade — don't skip this" · "One command family for Ubuntu, one for RHEL"
