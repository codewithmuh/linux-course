# Video 11 — Network Troubleshooting

**Module 3 · Networking · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "'It's not connecting.' Vague. Useless. By the end of this video you'll turn that into an exact answer: what's listening, what's blocked, and where the packets die."

## What you'll learn
- What's listening on which port: `ss`, `netstat`
- DNS debugging: `dig`, `nslookup`
- Path tracing: `traceroute`
- Manual port testing: `nc` (netcat)

## 1. 🎨 Animated slides (3–5 min)
- The troubleshooting ladder: is the host up? is the port open? is DNS right? is a firewall blocking?
- Listening sockets vs established connections
- Where `traceroute` fits (finding *where* it breaks)

## 2. 💻 Hands-on demo (10–15 min)
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

## 3. 🏢 Real production example
"App can't reach the database." Walk the ladder: `nc -zv db-host 5432` (port open?), `dig db-host` (DNS resolving?), `ss -tulpn` on the DB box (is Postgres actually listening?). Pinpoint the break in under a minute.

## 4. 📝 Exercise / challenge
- Use `ss -tulpn` to list every listening service on your box, then use `nc -zv` to test whether a remote host's port 443 is reachable.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `ss -tulpn` | What's listening (+ process) |
| `dig name +short` | Quick DNS answer |
| `traceroute host` | Where the path breaks |
| `nc -zv host port` | Is a port open |

## 6. 🎯 Next-lesson preview
→ **Video 12: SSH & Remote Servers** — you can diagnose the network; now let's connect to and move files between servers securely.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Network Troubleshooting in Linux (ss, dig, nc, traceroute)
- **Primary keyword:** linux network troubleshooting
- **Thumbnail idea:** A red "connection refused" with `nc -zv` diagnosing it
- **Shorts to cut:** "ss -tulpn: see everything listening" · "Test if a port is open with netcat"
