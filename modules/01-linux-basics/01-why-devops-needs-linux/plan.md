# Video 01 — Why Every DevOps Engineer Needs Linux

**Module 1 · Linux Basics · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Around 90% of the cloud runs on Linux. If you can't drive a Linux terminal, you can't do DevOps. In the next 18 minutes you'll go from zero to SSH-ing into your first server."

## What you'll learn
- What Linux actually is (kernel vs distribution)
- The major distributions and when each is used
- Why the cloud runs on Linux
- Install Ubuntu (or WSL on Windows)
- SSH into a remote server for the first time

## 1. 🎨 Animated slides (3–5 min)
- What is an OS → where the Linux kernel sits
- Kernel vs distribution (Ubuntu, Debian, RHEL, Alpine, Amazon Linux)
- Why cloud + containers are Linux-first (cost, control, ubiquity)
- The shell: what "the terminal" really is

## 2. 💻 Hands-on demo (10–15 min)
```bash
# Windows: install WSL
wsl --install -d Ubuntu

# Confirm you're on Linux
uname -a
cat /etc/os-release
whoami

# SSH into a remote server (e.g. a cheap cloud VM)
ssh ubuntu@<server-ip>
# then, on the server:
uname -a
exit
```

## 3. 🏢 Real production example
Every EC2 instance, container base image, and CI runner you'll touch is a Linux box you reach over SSH. Show a real cloud VM being launched and connected to.

## 4. 📝 Exercise / challenge
- Install Ubuntu/WSL and run `uname -a`, `whoami`, `cat /etc/os-release`. Spin up a free-tier cloud VM and SSH in.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `uname -a` | Kernel + system info |
| `cat /etc/os-release` | Which distro/version |
| `whoami` | Current user |
| `ssh user@host` | Connect to a remote server |

## 6. 🎯 Next-lesson preview
→ **Video 02: Linux File System & Navigation** — now that you're in, learn to move around like you own the place.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Why Every DevOps Engineer Needs Linux (Start Here)
- **Primary keyword:** linux for devops
- **Thumbnail idea:** Tux + a cloud, terminal prompt, "90% of the cloud"
- **Shorts to cut:** "Why the cloud runs on Linux" · "Install Linux in 60 seconds (WSL)"
