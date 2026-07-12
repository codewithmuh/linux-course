# Video 10 — Linux Networking

**Module 3 · Networking · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "A server nobody can reach is useless. Let's learn how traffic actually finds your machine — IP, DNS, and the tools to test it."

## What you'll learn
- IP addresses, ports, and interfaces
- DNS: how a name becomes an IP
- Test connectivity: `ping`, `curl`, `wget`
- Identity + interfaces: `hostname`, `ip addr`

## 1. 🎨 Animated slides (3–5 min)
- IP + port = a socket; public vs private IPs
- DNS resolution walkthrough (name → resolver → IP)
- The request path: your box → DNS → server:port

## 2. 💻 Hands-on demo (10–15 min)
```bash
hostname
hostname -I
ip addr            # interfaces + IPs (modern)
ip route           # default gateway

# DNS + reachability
ping -c 4 google.com
curl -I https://example.com          # headers only
curl https://api.github.com/zen
wget https://example.com/file.txt

cat /etc/hosts
cat /etc/resolv.conf                 # which DNS servers
```

## 3. 🏢 Real production example
Health-checking an API from the server: `curl -I` to confirm it's up and returning 200, `ping` to confirm the host is reachable, `ip addr` to confirm the box's own address.

## 4. 📝 Exercise / challenge
- Find your server's private and public IP, `curl -I` a website and read the status code, and add a custom entry to `/etc/hosts`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `ip addr` | Interfaces + IPs |
| `ping host` | Reachability test |
| `curl -I url` | HTTP headers / status |
| `hostname -I` | This box's IP(s) |
| `cat /etc/resolv.conf` | Configured DNS servers |

## 6. 🎯 Next-lesson preview
→ **Video 11: Network Troubleshooting** — when it *doesn't* connect, here's how you find out why.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux Networking Basics (IP, DNS, curl, ping)
- **Primary keyword:** linux networking basics
- **Thumbnail idea:** Laptop → DNS → server diagram with a curl status 200
- **Shorts to cut:** "curl -I: check any site's status" · "How DNS turns a name into an IP"
