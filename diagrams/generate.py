#!/usr/bin/env python3
"""Generate the 5 course module maps as MATCHING .excalidraw + .png files.

Tall vertical infographics: big type, one section per row, concept panels
between lesson cards. Every map is generated in TWO versions:

  diagrams/               compact spacing — embedded in the READMEs (GitHub)
  diagrams/presentation/  huge spacing — one container per screen, for
                          zooming + scrolling section by section on video

One display list per module -> rendered to PNG (Pillow) and to excalidraw
JSON, so the editable source and the preview can never drift apart.

Usage:   python3 generate.py          (needs: pillow, matplotlib)
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))

import matplotlib.font_manager as _fm  # matplotlib is only used to find its bundled DejaVu fonts
FONT_DIR = os.path.join(os.path.dirname(_fm.__file__), "mpl-data", "fonts", "ttf")

S = 2  # supersample factor for PNG rendering
BG = "#fbfcfe"

W = 1620          # canvas width for every module map
M = 30            # outer margin
CW = W - 2 * M    # full content width
GAP = 34          # vertical gap between sections; build_all() sets this per version
GAP_COMPACT = 34         # tight — reads well on GitHub, no wasted scroll
GAP_PRESENTATION = 460   # one container per 16:9 screen, nothing else in frame

TINT = {
    "#1971c2": "#e7f5ff", "#2f9e44": "#ebfbee", "#7048e8": "#f3f0ff",
    "#e8590c": "#fff4e6", "#0c8599": "#e3fafc", "#e03131": "#fff5f5",
    "#9c36b5": "#f8f0fc", "#495057": "#f1f3f5", "#c92a2a": "#fff5f5",
}
DEEP = {  # darker shade of each color, for text on light tints
    "#1971c2": "#1864ab", "#2f9e44": "#2b8a3e", "#7048e8": "#5f3dc4",
    "#e8590c": "#d9480f", "#0c8599": "#0b7285", "#e03131": "#c92a2a",
    "#9c36b5": "#862e9c", "#c92a2a": "#c92a2a",
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
    def __init__(self, w):
        self.w, self.h = w, 0
        self.items = []

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

    def chip(self, x, y, w, h, s, color, solid=False, mono=True, tsize=17, tcolor=None, sw=2.5):
        fill = color if solid else TINT.get(color, "#ffffff")
        self.rect(x, y, w, h, stroke=color, fill=fill, sw=sw, radius=10)
        lines = s.split("\n")
        block_h = len(lines) * tsize * 1.25
        tc = tcolor or ("#ffffff" if solid else DARK)
        self.text(x + w / 2, y + (h - block_h) / 2, s, tsize, tc,
                  kind=("mono" if mono else "sans"), align="center")


# ---------------------------------------------------------------- composites
def vheader(sc, y, color, kicker, title, subtitle):
    h = 150
    sc.rect(M, y, CW, h, stroke=color, fill=color, radius=18)
    sc.text(M + 40, y + 22, kicker, 20, "#ffffff", kind="mono")
    sc.text(M + 40, y + 52, title, 44, "#ffffff", bold=True)
    sc.text(M + 42, y + 112, subtitle, 21, "#e9ecef")
    return y + h + GAP


def tip_row(sc, x, y, color, text):
    sc.rect(x, y, 58, 27, stroke=color, fill=color, radius=13)
    sc.text(x + 29, y + 5.5, "TIP", 13, "#ffffff", bold=True, align="center")
    sc.text(x + 74, y + 3, text, 16.5, DEEP.get(color, color))
    return y + 27


def lesson_vcard(sc, y, num, title, color, intro, rows, tip):
    """Full-width lesson card. rows = [(cmd, comment)]; returns new y."""
    intro_lines = intro.split("\n")
    box_h = 22 + len(rows) * 34 + 14
    h = 86 + len(intro_lines) * 26 + 12 + box_h + 16 + 27 + 24
    sc.rect(M, y, CW, h, stroke=color, fill="#ffffff", sw=3, radius=16)
    sc.ellipse(M + 30, y + 22, 40, 40, stroke=color, fill=color)
    sc.text(M + 50, y + 31, num, 17, "#ffffff", kind="mono", bold=True, align="center")
    sc.text(M + 88, y + 24, title, 30, color, bold=True)
    sc.line(M + 30, y + 74, M + CW - 30, y + 74, color, sw=1.5)
    ty = y + 88
    for ln in intro_lines:
        sc.text(M + 34, ty, ln, 19.5, GRAY)
        ty += 26
    # command box
    bx, by, bw = M + 34, ty + 12, CW - 68
    sc.rect(bx, by, bw, box_h, stroke=color, fill=TINT[color], sw=2, radius=10)
    ccol = max(measure(c, 19, "mono") for c, _ in rows) + 64
    ry = by + 18
    for cmd, comment in rows:
        sc.text(bx + 28, ry, cmd, 19, DARK, kind="mono")
        if comment:
            sc.text(bx + 28 + ccol, ry + 1.5, "# " + comment, 17, LGRAY, kind="mono")
        ry += 34
    tip_row(sc, bx, by + box_h + 16, color, tip)
    return y + h + GAP


def vpanel(sc, y, h, title, color, tsize=22):
    """Full-width concept panel; returns content-area top y."""
    sc.rect(M, y, CW, h, stroke=color, fill="#ffffff", sw=2.5, radius=16)
    sc.rect(M, y, CW, 46, stroke=color, fill=color, radius=16,
            corners=(True, True, False, False))
    sc.text(M + 24, y + 10, title, tsize, "#ffffff", bold=True)
    return y + 46


def decoder_panel(sc, y, color, pairs):
    """'Command names, decoded' — two columns of cmd = full English form."""
    rows = (len(pairs) + 1) // 2
    ph = 46 + 26 + rows * 36 + 20
    cy = vpanel(sc, y, ph, "Command names, decoded — they are just short English words", color)
    col_x = [M + 70, W / 2 + 40]
    for i, (cmd, meaning) in enumerate(pairs):
        cx = col_x[i // rows]
        ry = cy + 24 + (i % rows) * 36
        sc.text(cx, ry, cmd, 18.5, DARK, kind="mono")
        sc.text(cx + 230, ry + 1, "= " + meaning, 17, GRAY)
    return y + ph + GAP


def outcome_banner(sc, y, color, text):
    h = 62
    sc.rect(M, y, CW, h, stroke=color, fill=TINT[color], sw=2.5, radius=14)
    sc.text(W / 2, y + 18, text, 21, DEEP.get(color, color), bold=True, align="center")
    return y + h


def flow_centered(sc, cx, y, items, h=56, gap=34, tsize=18, pad=30):
    widths = [max(measure(l, tsize, "mono") for l in s.split("\n")) + pad for s, _, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = cx - total / 2
    for i, ((s, color, solid), w) in enumerate(zip(items, widths)):
        sc.chip(x, y, w, h, s, color, solid=solid, tsize=tsize)
        x += w
        if i < len(items) - 1:
            sc.arrow(x + 5, y + h / 2, x + gap - 5, y + h / 2)
            x += gap


# ================================================================ MODULE 1
def module1():
    sc = Scene(W)
    y = vheader(sc, 30, "#1971c2", "MODULE 1  ·  4 LESSONS", "Linux Basics",
                "From zero to comfortable at the command line — the foundation everything else builds on.")

    # --- WHY panel (the question the whole course starts with) ---
    ph = 356
    cy = vpanel(sc, y, ph, "Why DevOps runs on Linux", "#1971c2")
    srcs = [("Cloud VMs\nAWS · Azure · GCP", "#1971c2"),
            ("Docker\ncontainers", "#0c8599"),
            ("CI/CD\nrunners", "#7048e8"),
            ("Kubernetes\nnodes", "#2f9e44")]
    gx = [M + 50, M + 370]
    gy = [cy + 26, cy + 106]
    k = 0
    for r in range(2):
        for c in range(2):
            s, col = srcs[k]; k += 1
            sc.chip(gx[c], gy[r], 296, 66, s, col, tsize=18, mono=False)
    lx, ly, lw, lh = M + 790, cy + 52, 210, 94
    sc.arrow(M + 678, gy[0] + 33, lx - 12, ly + 30)
    sc.arrow(M + 678, gy[1] + 33, lx - 12, ly + 62)
    sc.rect(lx, ly, lw, lh, stroke="#1971c2", fill="#1971c2", radius=14)
    sc.text(lx + lw / 2, ly + 16, "LINUX", 30, "#ffffff", kind="mono", bold=True, align="center")
    sc.text(lx + lw / 2, ly + 58, "one OS under all of it", 15, "#d0ebff", align="center")
    sc.arrow(lx + lw + 12, ly + lh / 2, lx + lw + 66, ly + lh / 2)
    sc.chip(lx + lw + 78, ly + 4, 370, 86, "You — over SSH, with the\ncommands in this course", "#e8590c", tsize=18, mono=False)
    rx = M + 50
    for s, col in [("Free", "#2f9e44"), ("Scriptable", "#1971c2"),
                   ("Stable for years", "#7048e8"), ("Same on every cloud", "#e8590c")]:
        wch = measure(s, 17.5, "sans") + 30
        sc.chip(rx, cy + 208, wch, 44, s, col, tsize=17.5, mono=False)
        rx += wch + 16
    sc.text(rx + 18, cy + 218, "→  more than 9 out of 10 cloud servers run Linux.", 19, GRAY)
    sc.text(M + 50, cy + 272, "Docker, Kubernetes, CI/CD, AWS — all of them expect you to know Linux. That is why this course comes first.",
            18, GRAY)
    y += ph + GAP

    # --- The stack ---
    ph = 424
    cy = vpanel(sc, y, ph, "How Linux is put together — the stack", "#1971c2")
    stack = [("You  ·  your shell, commands & tools", "#1971c2"),
             ("Distribution  ·  Ubuntu / RHEL / Alpine  —  packages & defaults", "#2f9e44"),
             ("Linux kernel  ·  talks to the hardware for you", "#7048e8"),
             ("Hardware  ·  CPU · RAM · Disk · Network", "#e8590c")]
    bw = 980
    bx = W / 2 - bw / 2
    by = cy + 24
    for i, (s, col) in enumerate(stack):
        sc.chip(bx, by, bw, 58, s, col, tsize=19.5, mono=False)
        if i < 3:
            sc.arrow(W / 2, by + 58 + 4, W / 2, by + 58 + 28)
        by += 58 + 32
    y += ph + GAP

    # --- Lesson 01 ---
    y = lesson_vcard(sc, y, "01", "Why DevOps Needs Linux", "#1971c2",
        "What Linux is, which distributions matter, and your first SSH into a real server.",
        [("uname -a", "kernel + architecture"),
         ("cat /etc/os-release", "which distribution"),
         ("whoami", "who am I logged in as"),
         ("ssh user@server-ip", "connect to a remote server"),
         ("wsl --install -d Ubuntu", "(Windows) WSL + Ubuntu in one"),
         ("multipass launch · shell", "(macOS) local Ubuntu VM")],
        "Every cloud VM, container and CI runner is a Linux machine you reach over SSH.")

    # --- Filesystem ---
    ph = 324
    cy = vpanel(sc, y, ph, "The filesystem — everything hangs off  /", "#2f9e44")
    rx0, ry0 = W / 2 - 38, cy + 20
    sc.rect(rx0, ry0, 76, 52, stroke="#2f9e44", fill="#2f9e44", radius=12)
    sc.text(rx0 + 38, ry0 + 12, "/", 24, "#ffffff", kind="mono", bold=True, align="center")
    kids = [("/etc", "config"), ("/var", "logs & data"), ("/home", "user files"),
            ("/usr", "software"), ("/tmp", "temp files")]
    kw, kgap = 170, 40
    total = len(kids) * kw + (len(kids) - 1) * kgap
    kx = W / 2 - total / 2
    ky = cy + 136
    for name, label in kids:
        sc.line(W / 2, ry0 + 52, kx + kw / 2, ky, LGRAY, sw=1.8)
        sc.chip(kx, ky, kw, 52, name, "#2f9e44", tsize=20)
        sc.text(kx + kw / 2, ky + 62, label, 16, LGRAY, align="center")
        kx += kw + kgap
    sc.text(W / 2, cy + 240, "No drive letters. One tree — learn it once and you will never feel lost on a server.",
            19, GRAY, align="center")
    y += ph + GAP

    # --- Lesson 02 ---
    y = lesson_vcard(sc, y, "02", "File System & Navigation", "#2f9e44",
        "Where things live, and how to move around, create, copy and delete.",
        [("pwd", "where am I"),
         ("ls -lah", "list: long + hidden + sizes"),
         ("cd /var/log", "move around   (cd -  = go back)"),
         ("mkdir -p app/logs", "create nested folders"),
         ("cp · mv · rm", "copy / move / delete"),
         ("find / -name '*.log'", "find files anywhere")],
        "Debugging a service is mostly navigation: cd /etc/nginx, then cd /var/log/nginx.")

    # --- Lesson 03 ---
    y = lesson_vcard(sc, y, "03", "Working with Files", "#7048e8",
        "Read, edit and search files — then chain small tools together with pipes.",
        [("cat · less · head · tail", "view a file"),
         ("tail -f app.log", "watch a log live"),
         ("nano file", "simple editor   (vim: i  Esc  :wq)"),
         ("grep -rin 'error' /var/log", "search inside files"),
         ("cmd1 | cmd2", "pipe: output → next input"),
         ("cmd > file   ·   cmd >> file", "write / append to a file")],
        "tail -f plus grep -i error is how most production problems are found.")

    # --- The pipe ---
    ph = 236
    cy = vpanel(sc, y, ph, "The pipe — small tools, chained into one answer", "#e8590c")
    flow_centered(sc, W / 2, cy + 26, [
        ("cat access.log", "#e8590c", False),
        ("grep -i error", "#e8590c", False),
        ("sort", "#e8590c", False),
        ("uniq -c", "#e8590c", False),
        ("sort -rn", "#e8590c", False),
        ("top 10 errors", "#c92a2a", False),
    ], h=58, gap=36, tsize=18)
    sc.text(W / 2, cy + 112, "One line finds the most common errors in a log — no extra tools needed.",
            19, GRAY, align="center")
    sc.text(W / 2, cy + 144, "Each tool does one small job well. That is the whole idea of the shell.",
            19, GRAY, align="center")
    y += ph + GAP

    # --- Lesson 04 ---
    y = lesson_vcard(sc, y, "04", "Text Processing", "#e8590c",
        "Turn messy command output into exactly the data you want.",
        [("sort | uniq -c | sort -rn", "rank by frequency"),
         ("cut -d: -f1 /etc/passwd", "take one column"),
         ("awk -F: '{print $1}'", "fields + filters + math"),
         ("awk '$3 >= 1000'", "keep matching rows only"),
         ("sed 's/old/new/g' file", "find & replace"),
         ("sed -i 's/a/b/g' file", "edit the file in place")],
        "awk over an access log gives you the top 10 client IPs in seconds.")

    y = decoder_panel(sc, y, "#1971c2", [
        ("pwd", "print working directory"),
        ("ls  ·  cd", "list  ·  change directory"),
        ("mkdir", "make directory"),
        ("cp · mv · rm", "copy · move · remove"),
        ("cat", "concatenate — joins files"),
        ("grep", "global regular expression print"),
        ("wc", "word count"),
        ("sed", "stream editor"),
        ("awk", "its creators: Aho, Weinberger, Kernighan"),
        ("ssh", "Secure Shell"),
        ("uname", "Unix name"),
        ("wsl", "Windows Subsystem for Linux"),
    ])
    y = outcome_banner(sc, y, "#1971c2",
        "By the end of Module 1 — you can navigate a server, manage files, and shape text output.")
    sc.h = y + 50
    return sc, "module-1-linux-basics"


# ================================================================ MODULE 2
def module2():
    sc = Scene(W)
    y = vheader(sc, 30, "#0c8599", "MODULE 2  ·  5 LESSONS", "Linux Administration",
                "Run a real system — users, permissions, processes, services, logs and packages.")

    y = lesson_vcard(sc, y, "05", "Users & Groups", "#1971c2",
        "Who can log in — and who is allowed to use root power.",
        [("id  ·  whoami  ·  groups", "who am I"),
         ("useradd -m -s /bin/bash u", "create a user (+ home + shell)"),
         ("passwd u", "set the password"),
         ("usermod -aG sudo u", "allow sudo"),
         ("sudo -u u whoami", "run one command as user u"),
         ("/etc/passwd · /etc/group", "where users and groups live")],
        "Log in as a normal user. Borrow root power with sudo only for the command that needs it.")

    y = lesson_vcard(sc, y, "06", "Linux Permissions", "#2f9e44",
        "Read -rwxr-xr--, then control who can read, write and run every file.",
        [("ls -l file", "see the permissions"),
         ("chmod +x script.sh", "make it executable"),
         ("chmod 600 ~/.ssh/id_ed25519", "lock a secret down"),
         ("chmod -R 755 /var/www/html", "folders + scripts"),
         ("chown deploy:deploy app.log", "change the owner"),
         ("chmod g+s shared/", "SGID: new files inherit the group")],
        "An SSH key that other users can read is rejected — chmod 600 fixes it.")

    # --- permissions decoder ---
    ph = 330
    cy = vpanel(sc, y, ph, "Reading  -rwxr-xr--   =   chmod 754", "#2f9e44")
    bits = [("-", "#7048e8", "type", 70), ("rwx", "#1971c2", "user (7)", 160),
            ("r-x", "#2f9e44", "group (5)", 160), ("r--", "#e8590c", "other (4)", 160)]
    total = sum(b[3] for b in bits) + 3 * 26
    bx = W / 2 - total / 2
    for s, col, lab, wch in bits:
        sc.chip(bx, cy + 24, wch, 56, s, col, solid=True, tsize=25)
        sc.text(bx + wch / 2, cy + 90, lab, 17, GRAY, align="center")
        bx += wch + 26
    sc.text(W / 2, cy + 134, "r = read (4)     w = write (2)     x = execute (1)     →     add them up per group.",
            19.5, DARK, align="center")
    sc.text(W / 2, cy + 174, "600  keys & secrets        644  config files        755  scripts & folders",
            19, GRAY, kind="mono", align="center")
    sc.rect(W / 2 - 340, cy + 214, 680, 44, stroke="#2f9e44", fill="#ebfbee", sw=2, radius=10)
    sc.text(W / 2, cy + 225, "SUID = run as owner · SGID = inherit group · sticky = /tmp", 17, "#2b8a3e",
            kind="mono", align="center")
    y += ph + GAP

    y = lesson_vcard(sc, y, "07", "Process Management", "#7048e8",
        "Every running program is a process with an ID — find it, watch it, stop it.",
        [("ps aux | grep nginx", "find a process"),
         ("top   /   htop", "live CPU + memory monitor"),
         ("sleep 300 &", "run in the background"),
         ("jobs · fg · bg · Ctrl-Z", "switch fore/background"),
         ("kill <pid>", "polite stop  (SIGTERM · 15)"),
         ("kill -9 <pid>", "force stop   (SIGKILL · 9)")],
        "Always try kill first. Use kill -9 only when the process will not stop.")

    # --- signals ---
    ph = 300
    cy = vpanel(sc, y, ph, "Stopping a process — two signals", "#7048e8")
    sc.chip(M + 120, cy + 30, 300, 76, "kill <pid>\nSIGTERM · 15", "#2f9e44", tsize=19)
    sc.text(M + 270, cy + 116, "polite — asks the process to stop", 16.5, GRAY, align="center")
    sc.chip(M + 500, cy + 30, 300, 76, "kill -9 <pid>\nSIGKILL · 9", "#c92a2a", tsize=19)
    sc.text(M + 650, cy + 116, "forced — last resort, no cleanup", 16.5, GRAY, align="center")
    sc.text(M + 920, cy + 30, "Process stuck at 100% CPU?", 21, DARK, bold=True)
    steps = [("1.", "top", "find it"), ("2.", "ps aux | grep", "confirm it"),
             ("3.", "kill → kill -9", "only if it will not stop")]
    yy = cy + 76
    for n_, cmd, what in steps:
        sc.text(M + 924, yy, n_, 18, DARK, kind="mono")
        sc.text(M + 964, yy, cmd, 18, "#5f3dc4", kind="mono", bold=True)
        sc.text(M + 1204, yy, what, 17.5, GRAY)
        yy += 38
    y += ph + GAP

    y = lesson_vcard(sc, y, "08", "Services & Logs", "#e8590c",
        "systemd keeps your app alive — journalctl shows you what it is doing.",
        [("systemctl status nginx", "running? + latest logs"),
         ("systemctl start / stop svc", "right now"),
         ("systemctl enable --now svc", "now + on every boot"),
         ("systemctl restart svc", "after a deploy"),
         ("journalctl -u svc -f", "follow the logs live"),
         ("journalctl --since \"1h ago\"", "logs by time")],
        "start = running now. enable = starts on boot. enable --now = both at once.")

    # --- systemd panel ---
    ph = 232
    cy = vpanel(sc, y, ph, "systemd — start ≠ enable", "#e8590c")
    chips = [("start\nrunning now", "#1971c2"), ("enable\nstarts on boot", "#7048e8"),
             ("enable --now\nboth at once", "#2f9e44")]
    cx = M + 70
    for s, col in chips:
        sc.chip(cx, cy + 28, 290, 70, s, col, tsize=19, mono=False)
        cx += 290 + 60
    sc.rect(M + 70, cy + 126, CW - 140, 46, stroke="#e8590c", fill="#fff4e6", sw=2, radius=10)
    sc.text(W / 2, cy + 137, "Run any app as a service → it survives crashes and reboots.", 19,
            "#d9480f", bold=True, align="center")
    y += ph + GAP

    y = lesson_vcard(sc, y, "09", "Package Management", "#0c8599",
        "Install software the safe way — from repositories, with dependencies handled for you.",
        [("apt update", "refresh the package catalog"),
         ("apt upgrade -y", "install newer versions"),
         ("apt install -y htop", "install a package"),
         ("apt show nginx", "inspect before installing"),
         ("apt remove --purge htop", "remove + its config"),
         ("dnf / yum install pkg", "Red Hat family (RHEL, Amazon)")],
        "apt update refreshes the list, apt upgrade installs from it — always that order.")

    y = decoder_panel(sc, y, "#0c8599", [
        ("sudo", "superuser do"),
        ("useradd · usermod", "user add · user modify"),
        ("passwd", "password"),
        ("chmod", "change mode (the permissions)"),
        ("chown · chgrp", "change owner · change group"),
        ("ps", "process status"),
        ("PID", "process ID"),
        ("SIGTERM · SIGKILL", "signal terminate · signal kill"),
        ("systemctl", "system control"),
        ("journalctl", "journal control — systemd's log book"),
        ("apt", "Advanced Package Tool"),
        ("rpm", "Red Hat Package Manager"),
    ])
    y = outcome_banner(sc, y, "#0c8599",
        "By the end of Module 2 — you can run a server: users, permissions, processes, services, packages.")
    sc.h = y + 50
    return sc, "module-2-linux-administration"


# ================================================================ MODULE 3
def module3():
    sc = Scene(W)
    y = vheader(sc, 30, "#9c36b5", "MODULE 3  ·  3 LESSONS", "Networking",
                "Understand and troubleshoot how traffic reaches a server — and connect to it securely.")

    # --- request path ---
    ph = 296
    cy = vpanel(sc, y, ph, "How a request reaches your app", "#1971c2")
    flow_centered(sc, W / 2, cy + 28, [
        ("Your\nmachine", "#1971c2", False),
        ("DNS\nname → IP", "#7048e8", False),
        ("Firewall\n:443 open?", "#e8590c", False),
        ("Nginx\n:80 / :443", "#2f9e44", False),
        ("App\n:8000", "#0c8599", False),
    ], h=74, gap=42, tsize=18)
    sc.rect(M + 120, cy + 136, CW - 240, 84, stroke="#1971c2", fill="#e7f5ff", sw=2, radius=10)
    sc.text(M + 144, cy + 150, "DNS in one line:", 18, "#1971c2", bold=True)
    sc.text(M + 144, cy + 182, "a name (example.com) → resolver → an IP (93.184.216.34) → connect to IP:port",
            18, "#1864ab", kind="mono")
    y += ph + GAP

    y = lesson_vcard(sc, y, "10", "Linux Networking", "#1971c2",
        "IP addresses, ports and DNS — and the commands that prove a connection works.",
        [("hostname -I", "this machine's IP"),
         ("ip addr  ·  ip route", "interfaces + gateway"),
         ("ping -c 4 google.com", "is it reachable?"),
         ("curl -I https://site", "HTTP status, from any server"),
         ("wget https://site/file", "download a file"),
         ("cat /etc/resolv.conf", "which DNS servers I use")],
        "curl -I is the fastest \"is my API up?\" check that works on every server.")

    y = lesson_vcard(sc, y, "11", "Network Troubleshooting", "#e8590c",
        "\"It's not connecting\" is a list of questions — each one has a command that answers it.",
        [("ss -tulpn", "what is listening on which port?"),
         ("nc -zv host 443", "is the port open from here?"),
         ("dig +short name", "what does DNS answer?"),
         ("nslookup name", "DNS, the classic way"),
         ("traceroute host", "where does the path stop?")],
        "Stop guessing — check in order: host → port → DNS → listening → path.")

    # --- check in order ---
    ph = 372
    cy = vpanel(sc, y, ph, "“It won't connect” — check in order", "#e8590c")
    ladder = [("Is the host up?", "ping host", "#1971c2"),
              ("Is the port open?", "nc -zv host port", "#2f9e44"),
              ("Is DNS right?", "dig +short name", "#7048e8"),
              ("Is anything listening?", "ss -tulpn", "#e8590c"),
              ("Where does it stop?", "traceroute host", "#c92a2a")]
    yy = cy + 26
    for i, (q, cmd, col) in enumerate(ladder, 1):
        sc.ellipse(M + 90, yy, 38, 38, stroke=col, fill=col)
        sc.text(M + 109, yy + 8, str(i), 17, "#ffffff", kind="mono", bold=True, align="center")
        sc.text(M + 150, yy + 6, q, 20.5, DARK, bold=True)
        sc.text(M + 560, yy + 8, cmd, 19, GRAY, kind="mono")
        yy += 60
    y += ph + GAP

    y = lesson_vcard(sc, y, "12", "SSH & Remote Servers", "#7048e8",
        "Log in with no password — a private key on your machine, a public key on the server.",
        [("ssh-keygen -t ed25519", "make a key pair"),
         ("ssh-copy-id user@host", "install the public key"),
         ("ssh prod", "one word, via ~/.ssh/config"),
         ("scp app.tgz prod:/tmp/", "copy files over SSH"),
         ("sftp prod", "interactive file transfer")],
        "The private key never leaves your machine — that is the whole trick.")

    # --- ssh keys ---
    ph = 300
    cy = vpanel(sc, y, ph, "SSH — key-based login", "#7048e8")
    sc.chip(M + 160, cy + 40, 300, 104, "You\nprivate key\n(never leaves)", "#7048e8", tsize=19, mono=False)
    sc.arrow(M + 476, cy + 92, M + 596, cy + 92)
    sc.text(M + 536, cy + 56, "ssh-copy-id", 15.5, GRAY, kind="mono", align="center")
    sc.chip(M + 608, cy + 40, 330, 104, "Server\nauthorized_keys\n(public key)", "#2f9e44", tsize=19, mono=False)
    sc.text(M + 1020, cy + 44, "During login the server checks that you", 18, GRAY)
    sc.text(M + 1020, cy + 72, "hold the matching private key —", 18, GRAY)
    sc.text(M + 1020, cy + 100, "without you ever sending it.", 18, GRAY)
    sc.rect(M + 160, cy + 178, CW - 320, 46, stroke="#7048e8", fill="#f3f0ff", sw=2, radius=10)
    sc.text(W / 2, cy + 189, "Harden the server: disable password login + root login in sshd_config.",
            18, "#5f3dc4", bold=True, align="center")
    y += ph + GAP

    y = decoder_panel(sc, y, "#9c36b5", [
        ("IP", "Internet Protocol"),
        ("DNS", "Domain Name System"),
        ("ping", "named after the submarine sonar sound"),
        ("curl", "client for URLs"),
        ("wget", "web get"),
        ("ss", "socket statistics"),
        ("dig", "domain information groper"),
        ("nc", "netcat — like cat, over the network"),
        ("scp", "secure copy"),
        ("sftp", "SSH File Transfer Protocol"),
    ])
    y = outcome_banner(sc, y, "#9c36b5",
        "By the end of Module 3 — you can debug \"why can't I connect?\" step by step, and reach any server securely.")
    sc.h = y + 50
    return sc, "module-3-networking"


# ================================================================ MODULE 4
def module4():
    sc = Scene(W)
    y = vheader(sc, 30, "#2f9e44", "MODULE 4  ·  3 LESSONS", "Bash Scripting",
                "Turn repetitive command-line work into robust, production-ready automation.")

    y = lesson_vcard(sc, y, "13", "Bash Basics", "#1971c2",
        "A script is just the commands you already type, saved in a file.",
        [("#!/usr/bin/env bash", "first line: which interpreter"),
         ("name=\"Rashid\" · echo \"$name\"", "variables (always quote them)"),
         ("today=$(date +%F)", "command output → variable"),
         ("if [[ -z \"$name\" ]]; then … fi", "conditions"),
         ("for i in 1 2 3; do … done", "loops"),
         ("read -rp \"Name: \" name", "ask the user for input")],
        "chmod +x script.sh, then ./script.sh — that is the whole setup.")

    # --- anatomy ---
    ph = 372
    cy = vpanel(sc, y, ph, "Anatomy of a production script", "#1971c2")
    rows = [("#!/usr/bin/env bash", "shebang — which interpreter runs this", "#1971c2"),
            ("set -euo pipefail", "safety belt — stop on any error", "#c92a2a"),
            ("log() { … }   backup_one() { … }", "small named functions", "#2f9e44"),
            ("main logic — call the functions", "the actual work", "#7048e8"),
            ("exit 0   /   exit 1", "tell the caller: success or failure", "#e8590c")]
    yy = cy + 30
    for code, label, col in rows:
        sc.rect(M + 70, yy + 2, 12, 38, stroke=col, fill=col, radius=5)
        sc.text(M + 104, yy + 6, code, 20, DARK, kind="mono")
        sc.text(M + 760, yy + 9, label, 18, LGRAY)
        yy += 62
    y += ph + GAP

    y = lesson_vcard(sc, y, "14", "Advanced Bash", "#2f9e44",
        "Functions, arrays and error handling — the difference between a demo and a real tool.",
        [("f() { local x=\"$1\"; … }", "functions + local variables"),
         ("arr=(a b c) · \"${arr[@]}\"", "arrays + expand all items"),
         ("$1  $@  $#", "script arguments"),
         ("echo $?", "exit code of the last command"),
         ("set -euo pipefail", "fail fast, fail loudly"),
         ("trap cleanup EXIT", "cleanup that always runs")],
        "Exit code 0 means success, anything else means failure — scripts talk in exit codes.")

    # --- pipefail ---
    ph = 380
    cy = vpanel(sc, y, ph, "set -euo pipefail — the line that makes Bash safe", "#c92a2a")
    flags = [("-e", "exit the moment any command fails", "#c92a2a"),
             ("-u", "error on an unset variable — catches typos", "#e8590c"),
             ("-o pipefail", "a failure anywhere in a pipe fails the whole line", "#7048e8")]
    yy = cy + 30
    for flag, expl, col in flags:
        wch = measure(flag, 20, "mono") + 36
        sc.chip(M + 70, yy, wch, 50, flag, col, solid=True, tsize=20)
        sc.text(M + 290, yy + 12, expl, 19.5, DARK)
        yy += 70
    sc.rect(M + 70, yy + 8, CW - 140, 74, stroke="#c92a2a", fill="#fff5f5", sw=2, radius=10)
    sc.text(M + 94, yy + 20, "trap cleanup EXIT", 19.5, "#c92a2a", kind="mono", bold=True)
    sc.text(M + 94, yy + 48, "cleanup that always runs — success, error, or Ctrl-C. No leftover temp files or locks.",
            17, GRAY)
    y += ph + GAP

    y = lesson_vcard(sc, y, "15", "Automation Scripts", "#7048e8",
        "Four real scripts every server should have — ready to schedule with cron.",
        [("./backup.sh /etc /backups", "timestamped tar, keep the last 7"),
         ("./healthcheck.sh", "warn at CPU / RAM / disk limits"),
         ("./logclean.sh /var/log/app", "gzip old logs, delete ancient ones"),
         ("./monitor.sh >> monitor.log", "one-line health snapshot")],
        "Config at the top, functions below, a clear exit code at the end — every time.")

    # --- cron ---
    ph = 372
    cy = vpanel(sc, y, ph, "Scripts → cron → servers that run themselves", "#7048e8")
    scripts = [("backup.sh", "#2f9e44"), ("healthcheck.sh", "#e8590c"),
               ("logclean.sh", "#1971c2"), ("monitor.sh", "#0c8599")]
    yy = cy + 30
    for s, col in scripts:
        sc.chip(M + 100, yy, 230, 46, s, col, tsize=18)
        sc.arrow(M + 340, yy + 23, M + 470, cy + 128)
        yy += 60
    sc.chip(M + 480, cy + 92, 220, 74, "crontab\n*/15 * * * *", "#7048e8", solid=True, tsize=18)
    sc.arrow(M + 712, cy + 129, M + 790, cy + 129)
    sc.chip(M + 800, cy + 98, 170, 62, "logs &\nalerts", "#c92a2a", tsize=17.5, mono=False)
    sc.text(M + 1060, cy + 92, "*/15 * * * *", 19, "#5f3dc4", kind="mono", bold=True)
    sc.text(M + 1060, cy + 124, "= every 15 minutes, forever —", 17.5, GRAY)
    sc.text(M + 1060, cy + 150, "no human needed.", 17.5, GRAY)
    sc.text(M + 100, cy + 292, "cron field order:   minute  hour  day  month  weekday", 19, DARK, kind="mono")
    y += ph + GAP

    y = decoder_panel(sc, y, "#2f9e44", [
        ("bash", "Bourne Again SHell — a pun on Steve Bourne's shell"),
        ("#!  (shebang)", "\"sharp\" (#) + \"bang\" (!)"),
        ("$?", "exit code of the last command"),
        ("$@  ·  $#", "all arguments · how many arguments"),
        ("echo", "prints back what you give it"),
        ("trap", "catch a signal and run cleanup"),
    ])
    y = outcome_banner(sc, y, "#2f9e44",
        "By the end of Module 4 — you write scripts that are safe to run with nobody watching.")
    sc.h = y + 50
    return sc, "module-4-bash-scripting"


# ================================================================ MODULE 5
def module5():
    sc = Scene(W)
    y = vheader(sc, 30, "#e03131", "MODULE 5  ·  3 LESSONS  ·  CAPSTONE", "Linux for DevOps",
                "Apply everything on the real job — scheduling, a working toolkit, then deploy a production server.")

    y = lesson_vcard(sc, y, "16", "Linux in Real DevOps", "#1971c2",
        "The recurring jobs of a real server: schedule work, control the environment, watch the disks.",
        [("crontab -e  →  */15 * * * * cmd", "run it every 15 minutes"),
         ("export APP_ENV=production", "env var for this session"),
         ("echo 'export …' >> ~/.bashrc", "make it permanent"),
         ("df -h", "which disk is full?"),
         ("du -sh /var/* | sort -rh", "what filled it?"),
         ("tar -czf logs.tgz dir/", "archive + compress")],
        "df answers \"which disk is full\" — du answers \"what inside it is big\".")

    y = lesson_vcard(sc, y, "17", "Production Linux Tasks", "#e8590c",
        "One script with subcommands for the checks you run every single day.",
        [("./ops.sh cpu", "load right now"),
         ("./ops.sh ram", "memory pressure"),
         ("./ops.sh disk", "df + biggest folders"),
         ("./ops.sh logs nginx", "last hour of a service's logs"),
         ("./ops.sh ports", "everything listening"),
         ("./ops.sh restart nginx", "the only one that changes state")],
        "Reads are safe anytime. restart changes the system — keep that line clear in your head.")

    # --- ops hub ---
    ph = 420
    cy = vpanel(sc, y, ph, "ops.sh — the junior DevOps toolkit", "#e8590c")
    hx, hy = W / 2, cy + 172
    spokes = [("cpu", "#1971c2", -330, -92), ("ram", "#2f9e44", 0, -118), ("disk", "#7048e8", 330, -92),
              ("ports", "#9c36b5", -330, 92), ("logs", "#0c8599", 0, 118), ("restart", "#c92a2a", 330, 92)]
    for s, col, dx, dy in spokes:
        sc.line(hx, hy, hx + dx, hy + dy, LGRAY, sw=1.8)
    sc.chip(hx - 90, hy - 36, 180, 72, "ops.sh", "#e8590c", solid=True, tsize=22)
    for s, col, dx, dy in spokes:
        wch = measure(s, 19, "mono") + 44
        sc.chip(hx + dx - wch / 2, hy + dy - 26, wch, 52, s, col, tsize=19)
    sc.text(W / 2, cy + 330, "measure → locate → act.   This is the day-to-day work.", 19.5, GRAY, align="center")
    y += ph + GAP

    # --- capstone architecture ---
    ph = 620
    cy = vpanel(sc, y, ph, "Capstone architecture — a production Linux server", "#2f9e44")
    chain_x = M + 330
    sc.chip(chain_x - 110, cy + 24, 220, 64, "User / Admin", "#9c36b5", tsize=19, mono=False)
    sc.arrow(chain_x, cy + 94, chain_x, cy + 138)
    sc.text(chain_x + 20, cy + 102, "HTTP/HTTPS   ·   SSH (key only)", 16.5, GRAY)
    sc.chip(chain_x - 150, cy + 144, 300, 64, "Firewall + hardened SSH", "#c92a2a", tsize=18, mono=False)
    bx0, by0 = M + 80, cy + 246
    bw0, bh0 = CW - 160, 320
    sc.rect(bx0, by0, bw0, bh0, stroke="#2f9e44", fill="#f8fff9", sw=2.5, radius=14)
    sc.text(bx0 + bw0 - 26 - measure("Production server  (Ubuntu)", 19, "sans", True),
            by0 + 14, "Production server  (Ubuntu)", 19, "#2b8a3e", bold=True)
    sc.arrow(chain_x, cy + 214, chain_x, by0 + 56)
    sc.chip(chain_x - 110, by0 + 62, 220, 66, "Nginx\n:80 / :443", "#2f9e44", tsize=18)
    sc.arrow(chain_x, by0 + 134, chain_x, by0 + 178)
    sc.text(chain_x + 20, by0 + 142, "reverse proxy → 127.0.0.1:8000", 16.5, GRAY, kind="mono")
    sc.chip(chain_x - 140, by0 + 184, 280, 70, "sampleapp\nsystemd service", "#1971c2", tsize=18, mono=False)
    sc.text(chain_x, by0 + 266, "Restart=always → self-heals", 16.5, "#1971c2", align="center")
    rx = bx0 + 850
    sc.chip(rx, by0 + 56, 190, 62, "cron\n0 2 * * *", "#7048e8", tsize=17)
    sc.arrow(rx + 198, by0 + 87, rx + 258, by0 + 87)
    sc.chip(rx + 266, by0 + 60, 170, 56, "nightly\nbackups", "#e8590c", tsize=16.5, mono=False)
    sc.arrow(chain_x + 142, by0 + 219, rx + 60, by0 + 226, dashed=True)
    sc.text(rx - 120, by0 + 196, "logs", 15.5, LGRAY)
    sc.chip(rx, by0 + 200, 440, 54, "journald + ops.sh  →  monitoring", "#0c8599", tsize=17.5)
    y += ph + GAP

    y = lesson_vcard(sc, y, "18", "Capstone: Deploy a Production Server", "#2f9e44",
        "Take a bare Ubuntu server to production, using every skill in the course.",
        [("1. deploy user + sudo", "Module 2"),
         ("2. key-only SSH, no root login", "Module 3"),
         ("3. Nginx → app as a systemd service", "Modules 2 + 3"),
         ("4. nightly cron backups", "Modules 4 + 5"),
         ("5. journald + ops.sh monitoring", "Modules 2 + 5"),
         ("6. kill the app — watch systemd heal it", "the proof")],
        "Test ssh deploy@ip from a second terminal BEFORE you log out — never lock yourself out.")

    y = decoder_panel(sc, y, "#e03131", [
        ("cron", "from Greek chronos — time"),
        ("crontab", "cron table — your list of scheduled jobs"),
        ("df", "disk free"),
        ("du", "disk usage"),
        ("tar", "tape archive — from the tape-backup days"),
        ("gzip", "GNU zip"),
        ("daemon", "a program that runs in the background"),
        ("ops", "operations — the day-to-day work"),
    ])
    y = outcome_banner(sc, y, "#e03131",
        "Finish line — a secured, monitored, app-serving Linux server you built end to end.")
    sc.h = y + 50
    return sc, "module-5-linux-for-devops"


# ============================================================ RENDERERS
def render_png(sc, path):
    img = Image.new("RGB", (sc.w * S, int(sc.h) * S), BG)
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
                    wl = _mdraw.textlength(line, font=f)
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

    img = img.resize((sc.w, int(sc.h)), Image.LANCZOS)
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


def build_all(gap, out_dir, label):
    global GAP
    GAP = gap
    os.makedirs(out_dir, exist_ok=True)
    for build in (module1, module2, module3, module4, module5):
        sc, name = build()
        render_png(sc, os.path.join(out_dir, f"{name}.png"))
        render_excalidraw(sc, os.path.join(out_dir, f"{name}.excalidraw"))
        print(f"{label}  {name}: {sc.w}x{int(sc.h)}")


if __name__ == "__main__":
    build_all(GAP_COMPACT, OUT, "github      ")
    build_all(GAP_PRESENTATION, os.path.join(OUT, "presentation"), "presentation")
