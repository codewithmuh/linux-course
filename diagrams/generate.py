#!/usr/bin/env python3
"""Generate the 5 course module maps as MATCHING .excalidraw + .png files.

One display list per module -> rendered to PNG (PIL) and to excalidraw JSON,
so the editable source and the preview can never drift apart.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/rashid/linux-course/diagrams"
FONT_DIR = "/Users/rashid/.pyenv/versions/3.10.12/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf"
S = 2  # supersample factor for PNG rendering
BG = "#fbfcfe"

TINT = {
    "#1971c2": "#e7f5ff", "#2f9e44": "#ebfbee", "#7048e8": "#f3f0ff",
    "#e8590c": "#fff4e6", "#0c8599": "#e3fafc", "#e03131": "#fff5f5",
    "#9c36b5": "#f8f0fc", "#495057": "#f1f3f5", "#c92a2a": "#fff5f5",
}
DARK = "#343a40"
GRAY = "#495057"
LGRAY = "#868e96"

_fonts = {}
def font(kind, size, bold=False):
    key = (kind, size, bold)
    if key not in _fonts:
        name = {
            ("sans", False): "DejaVuSans.ttf",
            ("sans", True): "DejaVuSans-Bold.ttf",
            ("mono", False): "DejaVuSansMono.ttf",
            ("mono", True): "DejaVuSansMono-Bold.ttf",
        }[(kind, bold)]
        _fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _fonts[key]

_meas = Image.new("RGB", (8, 8))
_mdraw = ImageDraw.Draw(_meas)
def measure(text, size, kind="sans", bold=False):
    f = font(kind, size, bold)
    return max(_mdraw.textlength(line, font=f) for line in text.split("\n"))


class Scene:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.items = []

    # ---- primitives ----
    def rect(self, x, y, w, h, stroke, fill, sw=2.5, radius=14, corners=None, dashed=False):
        self.items.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke=stroke,
                               fill=fill, sw=sw, radius=radius, corners=corners, dashed=dashed))

    def ellipse(self, x, y, w, h, stroke, fill, sw=2.5):
        self.items.append(dict(kind="ellipse", x=x, y=y, w=w, h=h, stroke=stroke, fill=fill, sw=sw))

    def text(self, x, y, s, size, color=DARK, kind="sans", bold=False, align="left"):
        """y = top of the text block. align=center -> x is the center."""
        wpx = measure(s, size, kind, bold)
        if align == "center":
            x = x - wpx / 2
        lh = round(size * 1.25, 2)
        n = len(s.split("\n"))
        self.items.append(dict(kind="text", x=x, y=y, w=wpx, h=lh * n, text=s, size=size,
                               color=color, font=kind, bold=bold, align=align, lh=lh))
        return wpx

    def line(self, x1, y1, x2, y2, color, sw=2, dashed=False):
        self.items.append(dict(kind="line", x1=x1, y1=y1, x2=x2, y2=y2,
                               color=color, sw=sw, dashed=dashed))

    def arrow(self, x1, y1, x2, y2, color=LGRAY, sw=2.5, dashed=False):
        self.items.append(dict(kind="arrow", x1=x1, y1=y1, x2=x2, y2=y2,
                               color=color, sw=sw, dashed=dashed))

    # ---- composites ----
    def chip(self, x, y, w, h, s, color, solid=False, mono=True, tsize=17, tcolor=None, sw=2.5):
        fill = color if solid else TINT.get(color, "#ffffff")
        self.rect(x, y, w, h, stroke=color, fill=fill, sw=sw, radius=10)
        lines = s.split("\n")
        block_h = len(lines) * tsize * 1.25
        tc = tcolor or ("#ffffff" if solid else DARK)
        self.text(x + w / 2, y + (h - block_h) / 2, s, tsize, tc,
                  kind=("mono" if mono else "sans"), align="center")

    def flow(self, x, y, items, h=50, gap=34, tsize=16.5, pad=26):
        """items: list of (text, color, solid) chips joined by arrows. Returns end x."""
        cx = x
        for i, (s, color, solid) in enumerate(items):
            w = max(measure(l, tsize, "mono") for l in s.split("\n")) + pad
            self.chip(cx, y, w, h, s, color, solid=solid, tsize=tsize)
            cx += w
            if i < len(items) - 1:
                self.arrow(cx + 5, y + h / 2, cx + gap - 5, y + h / 2)
                cx += gap
        return cx


def header(sc, W, color, kicker, title, subtitle):
    sc.rect(30, 30, W - 60, 118, stroke=color, fill=color, radius=16)
    sc.text(70, 46, kicker, 18, "#ffffff", kind="mono")
    sc.text(70, 72, title, 38, "#ffffff", bold=True)
    sc.text(72, 121, subtitle, 19, "#e9ecef")


def lesson_card(sc, x, y, w, h, num, title, color, lines):
    sc.rect(x, y, w, h, stroke=color, fill="#ffffff", sw=2.5, radius=14)
    sc.ellipse(x + 20, y + 18, 34, 34, stroke=color, fill=color)
    sc.text(x + 37, y + 25, num, 16, "#ffffff", kind="mono", bold=True, align="center")
    sc.text(x + 66, y + 22, title, 23, color, bold=True)
    sc.line(x + 20, y + 62, x + w - 20, y + 62, color, sw=1.5)
    ty = y + 76
    for ln in lines:
        sc.text(x + 24, ty, ln, 18, DARK, kind="mono")
        ty += 28


def cards_row(sc, W, y, cards, h=250):
    n = len(cards)
    gap = 36
    w = (W - 60 - (n - 1) * gap) / n
    x = 30
    for i, (num, title, color, lines) in enumerate(cards):
        lesson_card(sc, x, y, w, h, num, title, color, lines)
        if i < n - 1:
            sc.arrow(x + w + 6, y + h / 2, x + w + gap - 6, y + h / 2)
        x += w + gap


def panel(sc, x, y, w, h, title, color, tsize=20):
    sc.rect(x, y, w, h, stroke=color, fill="#ffffff", sw=2.5, radius=14)
    sc.rect(x, y, w, 40, stroke=color, fill=color, radius=14, corners=(True, True, False, False))
    sc.text(x + 18, y + 9, title, tsize, "#ffffff", bold=True)


# ============================================================ MODULE 1
def module1():
    W, H = 1940, 1120
    sc = Scene(W, H)
    header(sc, W, "#1971c2", "MODULE 1  ·  4 LESSONS", "Linux Basics",
           "From zero to comfortable at the command line — the foundation everything else builds on.")
    cards_row(sc, W, 180, [
        ("01", "Why DevOps Needs Linux", "#1971c2",
         ["9/10 cloud servers = Linux", "kernel vs distribution", "Ubuntu · RHEL · Alpine",
          "wsl --install -d Ubuntu", "ssh user@host", "uname -a  ·  whoami"]),
        ("02", "File System & Navigation", "#2f9e44",
         ["pwd   ls -lah   cd", "mkdir -p   touch", "cp   mv   rm",
          "find / -name '*.log'", "paths:  /  ·  .  ·  ..  ·  ~"]),
        ("03", "Working with Files", "#7048e8",
         ["cat  less  head  tail", "tail -f   (follow logs)", "nano · vim (i Esc :wq)",
          "grep -rin 'error'", "pipes |   redirect > >> <"]),
        ("04", "Text Processing", "#e8590c",
         ["sort | uniq -c | sort -rn", "cut -d: -f1", "awk -F: '{print $1}'",
          "sed 's/old/new/g'", "paste    wc -l"]),
    ])

    # --- Row 1: WHY panel + Linux stack ---
    py, ph = 466, 300
    px, pw = 30, 1170
    panel(sc, px, py, pw, ph, "Why DevOps runs on Linux", "#1971c2")
    srcs = [("Cloud VMs\nAWS · Azure · GCP", "#1971c2"),
            ("Docker\ncontainers", "#0c8599"),
            ("CI/CD\nrunners", "#7048e8"),
            ("Kubernetes\nnodes", "#2f9e44")]
    gx = [px + 40, px + 285]
    gy = [py + 62, py + 132]
    k = 0
    for r in range(2):
        for c in range(2):
            s, col = srcs[k]; k += 1
            sc.chip(gx[c], gy[r], 215, 58, s, col, tsize=15.5, mono=False)
    # arrows into the Linux box
    lx, ly, lw, lh = px + 610, py + 88, 170, 74
    sc.arrow(px + 508, py + 91, lx - 10, ly + 26)
    sc.arrow(px + 508, py + 161, lx - 10, ly + 48)
    sc.rect(lx, ly, lw, lh, stroke="#1971c2", fill="#1971c2", radius=12)
    sc.text(lx + lw / 2, ly + 12, "LINUX", 24, "#ffffff", kind="mono", bold=True, align="center")
    sc.text(lx + lw / 2, ly + 44, "one OS under all of it", 12.5, "#d0ebff", align="center")
    sc.arrow(lx + lw + 10, ly + lh / 2, lx + lw + 62, ly + lh / 2)
    sc.chip(lx + lw + 72, ly + 4, 300, 66, "You — over SSH, with\nthe commands in this course", "#e8590c", tsize=15.5, mono=False)
    reasons = [("Free", "#2f9e44"), ("Scriptable", "#1971c2"), ("Stable for years", "#7048e8"), ("Same on every cloud", "#e8590c")]
    rx = px + 40
    for s, col in reasons:
        w = measure(s, 15, "sans") + 26
        sc.chip(rx, py + 212, w, 36, s, col, tsize=15, mono=False)
        rx += w + 14
    sc.text(rx + 16, py + 220, "→  more than 9 out of 10 cloud servers run Linux.", 16.5, GRAY)

    # --- Row 1b: The Linux stack ---
    px2, pw2 = 1230, 680
    panel(sc, px2, py, pw2, ph, "The Linux stack", "#1971c2")
    stack = [("You · shell & tools", "#1971c2"),
             ("Distribution  (apt, config, defaults)", "#2f9e44"),
             ("Linux kernel  (talks to hardware)", "#7048e8"),
             ("Hardware · CPU · RAM · Disk · NIC", "#e8590c")]
    bw = 520
    bx = px2 + (pw2 - bw) / 2
    by = py + 56
    for i, (s, col) in enumerate(stack):
        sc.chip(bx, by, bw, 42, s, col, tsize=15.5, mono=False)
        if i < 3:
            sc.arrow(bx - 28, by + 42 + 44, bx - 28, by + 42 + 6, color=LGRAY, sw=2)
        by += 58

    # --- Row 2: filesystem tree ---
    py2 = 796
    px3, pw3 = 30, 700
    panel(sc, px3, py2, pw3, ph, "Filesystem — everything hangs off  /", "#2f9e44")
    rx0, ry0 = px3 + pw3 / 2 - 30, py2 + 54
    sc.rect(rx0, ry0, 60, 40, stroke="#2f9e44", fill="#2f9e44", radius=10)
    sc.text(rx0 + 30, ry0 + 8, "/", 20, "#ffffff", kind="mono", bold=True, align="center")
    kids = [("/etc", "config"), ("/var", "logs"), ("/home", "users"), ("/usr", "software"), ("/tmp", "temp")]
    kw, kgap = 108, 22
    total = len(kids) * kw + (len(kids) - 1) * kgap
    kx = px3 + (pw3 - total) / 2
    ky = py2 + 158
    for name, label in kids:
        sc.line(rx0 + 30, ry0 + 40, kx + kw / 2, ky, LGRAY, sw=1.8)
        sc.chip(kx, ky, kw, 40, name, "#2f9e44", tsize=16)
        sc.text(kx + kw / 2, ky + 48, label, 13.5, LGRAY, align="center")
        kx += kw + kgap
    sc.text(px3 + pw3 / 2, py2 + 248, "No drive letters. One tree — learn it once, never feel lost on a server.",
            15.5, GRAY, align="center")

    # --- Row 2b: one-liner panel ---
    px4, pw4 = 760, 1150
    panel(sc, px4, py2, pw4, ph, "One line answers a real question — top errors in a log", "#e8590c")
    sc.flow(px4 + 34, py2 + 62, [
        ("cat access.log", "#e8590c", False),
        ("grep -i error", "#e8590c", False),
        ("sort", "#e8590c", False),
        ("uniq -c", "#e8590c", False),
        ("sort -rn", "#e8590c", False),
        ("top 10 errors", "#c92a2a", False),
    ], h=48, gap=32, tsize=16)
    sc.text(px4 + 36, py2 + 136, "|  the pipe — one command's output becomes the next one's input.", 16.5, GRAY, kind="sans")
    sc.text(px4 + 36, py2 + 168, "Small tools, chained — each does one job well. That is the whole idea of the shell.", 16.5, GRAY)
    sc.rect(px4 + 34, py2 + 216, pw4 - 68, 48, stroke="#1971c2", fill="#e7f5ff", sw=2, radius=10)
    sc.text(px4 + pw4 / 2, py2 + 229, "By the end of Module 1 you can navigate a server, manage files, and shape text output.",
            16.5, "#1971c2", align="center")
    return sc, "module-1-linux-basics"


# ============================================================ MODULE 2
def module2():
    W, H = 2040, 820
    sc = Scene(W, H)
    header(sc, W, "#0c8599", "MODULE 2  ·  5 LESSONS", "Linux Administration",
           "Run a real system — users, permissions, processes, services, logs and packages.")
    cards_row(sc, W, 180, [
        ("05", "Users & Groups", "#1971c2",
         ["sudo   (least privilege)", "useradd -m -s /bin/bash", "usermod -aG sudo u", "passwd  ·  id", "/etc/passwd"]),
        ("06", "Permissions", "#2f9e44",
         ["-rwxr-xr--", "chmod 755 · 644 · 600", "chown u:g   chgrp", "SUID · SGID · sticky"]),
        ("07", "Processes", "#7048e8",
         ["ps aux   ·   top / htop", "kill (15)   kill -9 (9)", "jobs · bg · fg · &", "Ctrl-Z  suspend"]),
        ("08", "Services & Logs", "#e8590c",
         ["systemctl start|status", "enable --now  (on boot)", "journalctl -u svc -f", "/var/log/…"]),
        ("09", "Package Mgmt", "#0c8599",
         ["apt update && upgrade", "apt install -y pkg", "dpkg -l   ·   rpm -qa", "dnf / yum  (RHEL)"]),
    ], h=240)

    py, ph = 466, 320
    # --- A: permissions ---
    panel(sc, 30, py, 610, ph, "Reading  -rwxr-xr--   =   chmod 754", "#2f9e44")
    bits = [("-", "#7048e8", "type", 56), ("rwx", "#1971c2", "user (7)", 128),
            ("r-x", "#2f9e44", "group (5)", 128), ("r--", "#e8590c", "other (4)", 128)]
    bx = 66
    for s, col, lab, wch in bits:
        sc.chip(bx, py + 58, wch, 46, s, col, solid=True, tsize=21)
        sc.text(bx + wch / 2, py + 112, lab, 14.5, GRAY, align="center")
        bx += wch + 20
    sc.text(64, py + 148, "r = read (4)    w = write (2)    x = execute (1)   →   add them up.", 16.5, DARK)
    sc.text(64, py + 180, "600 keys & secrets  ·  644 configs  ·  755 scripts & dirs", 14.5, GRAY, kind="mono")
    sc.rect(60, py + 216, 490, 58, stroke="#2f9e44", fill="#ebfbee", sw=2, radius=10)
    sc.text(78, py + 226, "chmod 600 ~/.ssh/id_ed25519", 16.5, "#2b8a3e", kind="mono")
    sc.text(78, py + 250, "SUID/SGID = run as owner / inherit group  ·  sticky = /tmp", 13.5, GRAY)

    # --- B: signals ---
    panel(sc, 672, py, 560, ph, "Stopping a process — two signals", "#7048e8")
    sc.chip(706, py + 60, 224, 62, "kill <pid>\nSIGTERM · 15", "#2f9e44", tsize=16.5)
    sc.text(706 + 112, py + 130, "polite — asks the process", 14, GRAY, align="center")
    sc.chip(972, py + 60, 224, 62, "kill -9 <pid>\nSIGKILL · 9", "#c92a2a", tsize=16.5)
    sc.text(972 + 112, py + 130, "forced — last resort", 14, GRAY, align="center")
    sc.text(706, py + 170, "Process stuck at 100% CPU?", 17.5, DARK, bold=True)
    steps = [("1.", "top", "find it"), ("2.", "ps aux", "confirm"), ("3.", "kill → -9", "only if it will not stop")]
    yy = py + 206
    for n, cmd, what in steps:
        sc.text(710, yy, n, 16, DARK, kind="mono")
        sc.text(744, yy, cmd, 16, "#5f3dc4", kind="mono", bold=True)
        sc.text(884, yy, what, 15.5, GRAY)
        yy += 32
    # --- C: systemd ---
    panel(sc, 1264, py, 746, ph, "systemd — start ≠ enable", "#e8590c")
    sc.chip(1298, py + 58, 200, 58, "start\nrunning now", "#1971c2", tsize=15.5, mono=False)
    sc.chip(1522, py + 58, 200, 58, "enable\nstarts on boot", "#7048e8", tsize=15.5, mono=False)
    sc.chip(1746, py + 58, 230, 58, "enable --now\nboth at once", "#2f9e44", tsize=15.5, mono=False)
    sc.text(1298, py + 140, "systemctl status svc", 16.5, DARK, kind="mono")
    sc.text(1560, py + 140, "● active (running)  →  up + recent logs", 15, "#2b8a3e")
    sc.text(1298, py + 176, "journalctl -u svc -f", 16.5, DARK, kind="mono")
    sc.text(1560, py + 176, "follow a service's logs live during a deploy", 15, GRAY)
    sc.rect(1298, py + 222, 678, 52, stroke="#e8590c", fill="#fff4e6", sw=2, radius=10)
    sc.text(1298 + 678 / 2, py + 237, "Run any app as a service → it survives crashes and reboots.", 16.5, "#d9480f", align="center")
    return sc, "module-2-linux-administration"


# ============================================================ MODULE 3
def module3():
    W, H = 1920, 820
    sc = Scene(W, H)
    header(sc, W, "#9c36b5", "MODULE 3  ·  3 LESSONS", "Networking",
           "Understand and troubleshoot how traffic reaches a server — and connect to it securely.")
    cards_row(sc, W, 180, [
        ("10", "Linux Networking", "#1971c2",
         ["IP  ·  DNS  ·  ports", "ping -c 4 host", "curl -I https://site", "wget · hostname -I", "ip addr   ·   ip route"]),
        ("11", "Network Troubleshooting", "#e8590c",
         ["ss -tulpn     listening?", "dig +short · nslookup", "traceroute    the path", "nc -zv host port  open?"]),
        ("12", "SSH & Remote Servers", "#7048e8",
         ["ssh-keygen -t ed25519", "ssh-copy-id user@host", "~/.ssh/config → ssh prod", "scp   ·   sftp"]),
    ], h=240)

    py, ph = 466, 320
    # --- A: request path ---
    panel(sc, 30, py, 900, ph, "How a request reaches your app", "#1971c2")
    sc.flow(64, py + 62, [
        ("Your\nmachine", "#1971c2", False),
        ("DNS\nname → IP", "#7048e8", False),
        ("Firewall\n:443 open?", "#e8590c", False),
        ("Nginx\n:80 / :443", "#2f9e44", False),
        ("App\n:8000", "#0c8599", False),
    ], h=62, gap=34, tsize=15.5)
    sc.text(64, py + 150, "curl -I → confirm a 200 · ping → confirm reachable · ip addr → the box's own IP",
            15.5, GRAY)
    sc.rect(62, py + 196, 836, 82, stroke="#1971c2", fill="#e7f5ff", sw=2, radius=10)
    sc.text(80, py + 208, "DNS in one line:", 15.5, "#1971c2", bold=True)
    sc.text(80, py + 238, "a name (example.com) → resolver → an IP (93.184.216.34) → connect to IP:port",
            15.5, "#1864ab", kind="mono")

    # --- B: check in order ---
    panel(sc, 962, py, 512, ph, "“It won't connect” — check in order", "#e8590c")
    ladder = [("Is the host up?", "ping", "#1971c2"),
              ("Is the port open?", "nc -zv host port", "#2f9e44"),
              ("Is DNS right?", "dig +short name", "#7048e8"),
              ("Is it listening?", "ss -tulpn", "#e8590c"),
              ("Where does it stop?", "traceroute host", "#c92a2a")]
    yy = py + 58
    for i, (q, cmd, col) in enumerate(ladder, 1):
        sc.ellipse(994, yy, 30, 30, stroke=col, fill=col)
        sc.text(1009, yy + 6, str(i), 14.5, "#ffffff", kind="mono", bold=True, align="center")
        sc.text(1040, yy + 4, q, 16, DARK, bold=True)
        sc.text(1250, yy + 5, cmd, 15.5, GRAY, kind="mono")
        yy += 50
    # --- C: SSH ---
    panel(sc, 1506, py, 384, ph, "SSH — key-based login", "#7048e8")
    sc.chip(1540, py + 58, 136, 74, "You\nprivate key\n(never leaves)", "#7048e8", tsize=13, mono=False)
    sc.arrow(1682, py + 95, 1724, py + 95)
    sc.chip(1730, py + 58, 152, 74, "Server\nauthorized_keys\n(public key)", "#2f9e44", tsize=12.5, mono=False)
    sc.text(1540, py + 152, "ssh-copy-id installs the\npublic key.", 15, GRAY)
    sc.text(1540, py + 202, "The private key proves who\nyou are — you never send it.", 15, GRAY)
    sc.rect(1538, py + 254, 322, 46, stroke="#7048e8", fill="#f3f0ff", sw=2, radius=10)
    sc.text(1552, py + 261, "Harden it: disable password\n+ root SSH login.", 13.5, "#5f3dc4")
    return sc, "module-3-networking"


# ============================================================ MODULE 4
def module4():
    W, H = 1920, 820
    sc = Scene(W, H)
    header(sc, W, "#2f9e44", "MODULE 4  ·  3 LESSONS", "Bash Scripting",
           "Turn repetitive command-line work into robust, production-ready automation.")
    cards_row(sc, W, 180, [
        ("13", "Bash Basics", "#1971c2",
         ["#!/usr/bin/env bash", "var=\"x\" · $var · $(cmd)", "if [[ cond ]]; then … fi", "for / while loops", "read -rp   input"]),
        ("14", "Advanced Bash", "#2f9e44",
         ["functions · local x=\"$1\"", "arrays  \"${arr[@]}\"", "args $1 $@ $#  ·  exit $?", "set -euo pipefail", "trap cleanup EXIT"]),
        ("15", "Automation Scripts", "#7048e8",
         ["backup.sh     tar + rotate", "healthcheck.sh CPU/RAM/disk", "logclean.sh   find -mtime", "monitor.sh    cron snapshot"]),
    ], h=240)

    py, ph = 466, 320
    # --- A: anatomy ---
    panel(sc, 30, py, 580, ph, "Anatomy of a production script", "#1971c2")
    rows = [("#!/usr/bin/env bash", "shebang", "#1971c2"),
            ("set -euo pipefail", "safety belt", "#c92a2a"),
            ("log() { … }   functions", "reusable blocks", "#2f9e44"),
            ("main logic", "the work", "#7048e8"),
            ("exit code  0 / non-0", "success / failure", "#e8590c")]
    yy = py + 58
    for code, label, col in rows:
        sc.rect(62, yy + 3, 10, 30, stroke=col, fill=col, radius=4)
        sc.text(88, yy + 6, code, 16.5, DARK, kind="mono")
        sc.text(400, yy + 8, label, 14.5, LGRAY)
        yy += 50
    # --- B: set -euo pipefail ---
    panel(sc, 642, py, 620, ph, "set -euo pipefail — the line that makes Bash safe", "#c92a2a")
    flags = [("-e", "exit the moment any command fails", "#c92a2a"),
             ("-u", "error on an unset variable (typo guard)", "#e8590c"),
             ("-o pipefail", "a failure anywhere in a pipe fails the line", "#7048e8")]
    yy = py + 58
    for flag, expl, col in flags:
        w = measure(flag, 16.5, "mono") + 28
        sc.chip(676, yy, w, 40, flag, col, solid=True, tsize=16.5)
        sc.text(676 + 150, yy + 10, expl, 15.5, DARK)
        yy += 56
    sc.rect(676, yy + 6, 552, 62, stroke="#c92a2a", fill="#fff5f5", sw=2, radius=10)
    sc.text(694, yy + 15, "trap cleanup EXIT", 16, "#c92a2a", kind="mono", bold=True)
    sc.text(694, yy + 41, "cleanup that always runs — even when the script fails.", 14, GRAY)
    # --- C: cron ---
    panel(sc, 1294, py, 596, ph, "Scripts → cron → servers that run themselves", "#7048e8")
    scripts = [("backup.sh", "#2f9e44"), ("healthcheck.sh", "#e8590c"), ("logclean.sh", "#1971c2"), ("monitor.sh", "#0c8599")]
    yy = py + 56
    for s, col in scripts:
        sc.chip(1328, yy, 172, 36, s, col, tsize=14.5)
        sc.arrow(1508, yy + 18, 1548, py + 128)
        yy += 46
    sc.chip(1556, py + 100, 150, 56, "crontab\n*/15 * * * *", "#7048e8", solid=True, tsize=14.5)
    sc.arrow(1714, py + 128, 1756, py + 128)
    sc.chip(1764, py + 104, 108, 48, "logs &\nalerts", "#c92a2a", tsize=14, mono=False)
    sc.text(1328, py + 250, "cron field order:  min hour day month weekday", 15.5, DARK, kind="mono")
    sc.text(1328, py + 282, "*/15 * * * *  =  every 15 minutes, forever.", 15.5, GRAY, kind="mono")
    return sc, "module-4-bash-scripting"


# ============================================================ MODULE 5
def module5():
    W, H = 1940, 910
    sc = Scene(W, H)
    header(sc, W, "#e03131", "MODULE 5  ·  3 LESSONS  ·  CAPSTONE", "Linux for DevOps",
           "Apply everything on the real job — scheduling, a working toolkit, then deploy a production server.")
    cards_row(sc, W, 180, [
        ("16", "Linux in Real DevOps", "#1971c2",
         ["cron  */15 * * * *", "env vars  ~/.bashrc", "df -h · du -sh | sort -rh", "tar -czf  ·  gzip"]),
        ("17", "Production Toolkit", "#e8590c",
         ["ops.sh cpu | ram | disk", "ops.sh restart <svc>", "ops.sh logs <svc>", "ops.sh ports"]),
        ("18", "Capstone Project", "#2f9e44",
         ["users + sudo", "hardened SSH", "Nginx + app service", "cron backups + monitoring"]),
    ], h=240)

    py, ph = 466, 330
    # --- A: ops.sh hub ---
    panel(sc, 30, py, 600, ph, "ops.sh — the junior DevOps toolkit", "#e8590c")
    hx, hy = 30 + 300, py + 168
    spokes = [("cpu", "#1971c2", -190, -66), ("ram", "#2f9e44", 0, -84), ("disk", "#7048e8", 190, -66),
              ("ports", "#9c36b5", -190, 62), ("logs", "#0c8599", 0, 84), ("restart", "#c92a2a", 190, 62)]
    for s, col, dx, dy in spokes:
        w = measure(s, 15.5, "mono") + 30
        sc.line(hx, hy, hx + dx, hy + dy, LGRAY, sw=1.8)
    sc.chip(hx - 62, hy - 26, 124, 52, "ops.sh", "#e8590c", solid=True, tsize=17)
    for s, col, dx, dy in spokes:
        w = measure(s, 15.5, "mono") + 30
        sc.chip(hx + dx - w / 2, hy + dy - 19, w, 38, s, col, tsize=15.5)
    sc.text(30 + 300, py + 288, "measure → locate → act.  This is the day-to-day work.", 15.5, GRAY, align="center")

    # --- B: capstone architecture ---
    panel(sc, 662, py, 1248, ph, "Capstone architecture — a production Linux server", "#2f9e44")
    sc.chip(694, py + 120, 130, 62, "User /\nAdmin", "#9c36b5", tsize=15, mono=False)
    sc.arrow(832, py + 151, 884, py + 151)
    sc.text(857, py + 98, "HTTP/HTTPS", 12.5, GRAY, align="center")
    sc.chip(892, py + 120, 168, 62, "Firewall +\nhardened SSH", "#c92a2a", tsize=14.5, mono=False)
    sc.text(976, py + 190, "SSH · key only", 12.5, GRAY, align="center")
    # inner server box
    sc.rect(1092, py + 54, 786, 252, stroke="#2f9e44", fill="#f8fff9", sw=2, radius=12)
    sc.text(1112, py + 62, "Production server  (Ubuntu)", 14.5, "#2b8a3e", bold=True)
    sc.arrow(1060, py + 151, 1112, py + 151)
    sc.chip(1120, py + 120, 128, 62, "Nginx\n:80 / :443", "#2f9e44", tsize=14.5)
    sc.arrow(1256, py + 151, 1308, py + 151)
    sc.text(1282, py + 122, "proxy", 12.5, GRAY, align="center")
    sc.chip(1316, py + 120, 190, 62, "sampleapp\nsystemd service", "#1971c2", tsize=14.5, mono=False)
    sc.text(1411, py + 190, "Restart=always → self-heals", 12.5, "#1971c2", align="center")
    sc.chip(1560, py + 92, 140, 52, "cron\n0 2 * * *", "#7048e8", tsize=14)
    sc.arrow(1708, py + 118, 1746, py + 118)
    sc.chip(1754, py + 92, 108, 52, "nightly\nbackups", "#e8590c", tsize=13.5, mono=False)
    sc.arrow(1506, py + 168, 1556, py + 224, dashed=True)
    sc.text(1462, py + 210, "logs", 12.5, LGRAY)
    sc.chip(1560, py + 208, 302, 48, "journald + ops.sh → monitoring", "#0c8599", tsize=14)
    # footer
    sc.rect(30, py + ph + 22, W - 60, 54, stroke="#e03131", fill="#fff5f5", sw=2.5, radius=12)
    sc.text(W / 2, py + ph + 36, "Finish line — a secured, monitored, app-serving Linux server you built end to end.",
            17.5, "#c92a2a", align="center")
    return sc, "module-5-linux-for-devops"


# ============================================================ RENDERERS
def render_png(sc, path):
    img = Image.new("RGB", (sc.w * S, sc.h * S), BG)
    d = ImageDraw.Draw(img)

    def dash_line(p1, p2, color, w):
        import math
        x1, y1 = p1; x2, y2 = p2
        L = math.hypot(x2 - x1, y2 - y1)
        if L == 0:
            return
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        pos, on = 0.0, True
        while pos < L:
            seg = min(10 * S if on else 7 * S, L - pos)
            if on:
                d.line([x1 + ux * pos, y1 + uy * pos, x1 + ux * (pos + seg), y1 + uy * (pos + seg)],
                       fill=color, width=w)
            pos += seg
            on = not on

    for it in sc.items:
        k = it["kind"]
        if k == "rect":
            box = [it["x"] * S, it["y"] * S, (it["x"] + it["w"]) * S, (it["y"] + it["h"]) * S]
            kwargs = dict(radius=it["radius"] * S, fill=it["fill"], outline=it["stroke"],
                          width=max(1, round(it["sw"] * S)))
            if it["corners"] is not None:
                kwargs["corners"] = it["corners"]
            d.rounded_rectangle(box, **kwargs)
        elif k == "ellipse":
            d.ellipse([it["x"] * S, it["y"] * S, (it["x"] + it["w"]) * S, (it["y"] + it["h"]) * S],
                      fill=it["fill"], outline=it["stroke"], width=max(1, round(it["sw"] * S)))
        elif k == "text":
            f = font(it["font"], round(it["size"] * S), it["bold"])
            lh = it["lh"] * S
            for i, line in enumerate(it["text"].split("\n")):
                if it["align"] == "center":
                    wl = _mdraw.textlength(line, font=font(it["font"], round(it["size"] * S), it["bold"]))
                    lx = it["x"] * S + (it["w"] * S - wl) / 2
                else:
                    lx = it["x"] * S
                d.text((lx, it["y"] * S + i * lh + 0.12 * lh), line, font=f, fill=it["color"])
        elif k == "line":
            if it["dashed"]:
                dash_line((it["x1"] * S, it["y1"] * S), (it["x2"] * S, it["y2"] * S),
                          it["color"], max(1, round(it["sw"] * S)))
            else:
                d.line([it["x1"] * S, it["y1"] * S, it["x2"] * S, it["y2"] * S],
                       fill=it["color"], width=max(1, round(it["sw"] * S)))
        elif k == "arrow":
            import math
            x1, y1, x2, y2 = it["x1"] * S, it["y1"] * S, it["x2"] * S, it["y2"] * S
            ang = math.atan2(y2 - y1, x2 - x1)
            hl = 9 * S
            bx, by = x2 - hl * math.cos(ang), y2 - hl * math.sin(ang)
            if it["dashed"]:
                dash_line((x1, y1), (bx, by), it["color"], max(1, round(it["sw"] * S)))
            else:
                d.line([x1, y1, bx, by], fill=it["color"], width=max(1, round(it["sw"] * S)))
            wa = 5.2 * S
            p1 = (bx + wa * math.sin(ang), by - wa * math.cos(ang))
            p2 = (bx - wa * math.sin(ang), by + wa * math.cos(ang))
            d.polygon([p1, p2, (x2, y2)], fill=it["color"])

    img = img.resize((sc.w, sc.h), Image.LANCZOS)
    img.save(path, optimize=True)


def render_excalidraw(sc, path):
    els = []
    n = [0]

    def base(type_, x, y, w, h, stroke, bg_, sw=2, extra=None):
        n[0] += 1
        el = {
            "version": 1, "versionNonce": n[0] * 104729 + 7, "isDeleted": False,
            "id": f"el{n[0]:04d}", "fillStyle": "solid", "strokeWidth": sw,
            "strokeStyle": "solid", "roughness": 0, "opacity": 100, "angle": 0,
            "strokeColor": stroke, "backgroundColor": bg_, "seed": n[0] * 7919 + 13,
            "groupIds": [], "frameId": None, "roundness": None, "boundElements": [],
            "updated": 1720800000000, "link": None, "locked": False,
            "type": type_, "x": round(x, 2), "y": round(y, 2),
            "width": round(w, 2), "height": round(h, 2),
        }
        if extra:
            el.update(extra)
        els.append(el)
        return el

    for it in sc.items:
        k = it["kind"]
        if k == "rect":
            base("rectangle", it["x"], it["y"], it["w"], it["h"], it["stroke"], it["fill"],
                 sw=round(it["sw"]), extra={"roundness": {"type": 3},
                                            "strokeStyle": "dashed" if it["dashed"] else "solid"})
        elif k == "ellipse":
            base("ellipse", it["x"], it["y"], it["w"], it["h"], it["stroke"], it["fill"],
                 sw=round(it["sw"]))
        elif k == "text":
            nlines = len(it["text"].split("\n"))
            base("text", it["x"], it["y"], it["w"], it["lh"] * nlines, it["color"], "transparent",
                 extra={"text": it["text"], "originalText": it["text"],
                        "fontSize": round(it["size"], 2),
                        "fontFamily": 3 if it["font"] == "mono" else 2,
                        "textAlign": it["align"], "verticalAlign": "top",
                        "containerId": None, "lineHeight": 1.25,
                        "baseline": round(it["size"] * 0.875, 2)})
        elif k in ("line", "arrow"):
            x1, y1, x2, y2 = it["x1"], it["y1"], it["x2"], it["y2"]
            el = base("arrow" if k == "arrow" else "line",
                      min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1),
                      it["color"], "transparent", sw=round(it["sw"]),
                      extra={"points": [[0, 0], [x2 - x1, y2 - y1]],
                             "lastCommittedPoint": None,
                             "startBinding": None, "endBinding": None,
                             "startArrowhead": None,
                             "endArrowhead": "arrow" if k == "arrow" else None,
                             "strokeStyle": "dashed" if it["dashed"] else "solid"})
            el["x"], el["y"] = round(x1, 2), round(y1, 2)

    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": els,
           "appState": {"gridSize": None, "viewBackgroundColor": BG},
           "files": {}}
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)


if __name__ == "__main__":
    for build in (module1, module2, module3, module4, module5):
        sc, name = build()
        render_png(sc, os.path.join(OUT, f"{name}.png"))
        render_excalidraw(sc, os.path.join(OUT, f"{name}.excalidraw"))
        print(f"{name}: {sc.w}x{sc.h}, {len(sc.items)} items")
