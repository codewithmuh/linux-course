# Network Troubleshooting

> [Linux for DevOps](../../README.md) · Module 3 — Networking

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- What's listening on which port: `ss`, `netstat`
- DNS debugging: `dig`, `nslookup`
- Path tracing: `traceroute`
- Manual port testing: `nc` (netcat)

## Concepts
"It's not connecting" is never one problem — it's a list of possible problems. Check them in order: is the **host** up? is the **port** open? is **DNS** resolving correctly? is a **firewall** blocking the path? Each question has one command that answers it, so you stop guessing and start proving.

It helps to know the difference between a **listening socket** (a service waiting for connections on a port) and an **established connection** (an active conversation already in progress). `ss` shows you both. When traffic leaves your machine but never arrives, `traceroute` shows you *where* along the path it dies.

## Commands
```bash
# what's listening
ss -tulpn                 # modern (t=tcp u=udp l=listen p=process n=numeric)
sudo netstat -tulpn       # classic equivalent

# DNS
dig example.com +short
dig example.com A
nslookup example.com

# path + port reachability
traceroute example.com
nc -zv example.com 443    # is the port open?
nc -zv 10.0.0.5 22        # can I reach SSH on this host?
```

## In production
An app can't reach its database. You check in order: `nc -zv db-host 5432` (is the port open?), `dig db-host` (is DNS resolving?), and `ss -tulpn` on the DB box (is Postgres actually listening?). That finds the exact break in under a minute.

## Practice
- Use `ss -tulpn` to list every listening service on your box.
- Use `nc -zv` to test whether a remote host's port 443 is reachable.

## Cheat sheet
| Command | What it does |
|---|---|
| `ss -tulpn` | What's listening (+ process) |
| `dig name +short` | Quick DNS answer |
| `traceroute host` | Where the path breaks |
| `nc -zv host port` | Is a port open |

---
← [Course home](../../README.md) · **Next:** [SSH & Remote Servers](../12-ssh-and-remote-servers/README.md)
