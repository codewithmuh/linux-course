# Package Management

> [Linux for DevOps](../../README.md) · Module 2 — Linux Administration

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- Debian/Ubuntu family: `apt`, `dpkg`
- Red Hat family: `yum`, `dnf`
- Repositories, updates, and why `apt update` before `apt upgrade`
- Searching, inspecting, and removing packages

## Concepts

A **package** is software bundled with everything it needs and a record of its dependencies. A **package manager** installs, updates, and removes packages for you — resolving those dependencies automatically instead of you downloading loose binaries.

Packages come from **repositories**: servers that host the software plus a metadata index. That's why `apt update` (refresh the index) comes *before* `apt upgrade` (install newer versions) — you refresh the catalog first, then act on it.

There are two big families you'll meet constantly:

| Family | Format | Tools |
|---|---|---|
| **Debian / Ubuntu** | `.deb` | `apt`, `dpkg` |
| **Red Hat / Fedora / Amazon Linux** | `.rpm` | `dnf`, `yum` |

## Commands
```bash
# Debian / Ubuntu   (apt = "Advanced Package Tool")
sudo apt update
sudo apt upgrade -y
sudo apt install -y htop tree jq
apt search nginx
apt show nginx
dpkg -l | grep nginx             # dpkg = "Debian package"
sudo apt remove --purge htop

# Red Hat / Fedora / Amazon Linux   (dnf = "Dandified YUM", yum = "Yellowdog Updater, Modified")
sudo dnf update -y
sudo dnf install -y htop
sudo yum install -y git          # older systems
rpm -qa | grep git               # rpm = "Red Hat Package Manager"
```

## What the names mean

| Command | Stands for |
|---|---|
| `apt` | **A**dvanced **P**ackage **T**ool |
| `dpkg` | **D**ebian **p**ac**k**a**g**e |
| `yum` | **Y**ellowdog **U**pdater, **M**odified |
| `dnf` | **D**andified **YUM** — the newer yum |
| `rpm` | **R**ed Hat **P**ackage **M**anager |

## In production
`apt update && apt install ...` is the first lines of nearly every server bootstrap script, Dockerfile, and Ansible playbook. It's how a bare base image picks up the exact tools it needs before anything else runs.

## Practice
- Update your system, install `tree` and `jq`, inspect one of them with `apt show`, then cleanly remove it with `--purge`.

## Cheat sheet
| Command | What it does |
|---|---|
| `apt update` | Refresh package index |
| `apt install -y pkg` | Install |
| `apt remove --purge pkg` | Remove + config |
| `dpkg -l` / `rpm -qa` | List installed packages |
| `dnf install -y pkg` | Install (RHEL/Fedora) |

---
← [Course home](../../README.md) · **Next:** [Linux Networking](../../03-networking/10-linux-networking/README.md)
