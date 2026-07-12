# Video 03 — Working with Files

**Module 1 · Linux Basics · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "You're SSH'd into a broken server. No GUI. Just you, the logs, and these commands. Let's make sure you can read them."

## What you'll learn
- View files: `cat`, `less`, `head`, `tail` (incl. `tail -f`)
- Edit files: `nano` (beginner) and `vim` (survival basics)
- Search inside files: `grep`
- Chain commands: pipes `|` and redirection `>`, `>>`, `<`

## 1. 🎨 Animated slides (3–5 min)
- stdin / stdout / stderr — the three streams
- How a pipe connects one command's output to the next's input
- Redirection: file in, file out, append

## 2. 💻 Hands-on demo (10–15 min)
```bash
cat /etc/os-release
less /var/log/syslog          # q to quit
head -n 20 /var/log/syslog
tail -n 20 /var/log/syslog
tail -f /var/log/syslog       # live follow (Ctrl-C to stop)

# edit
nano notes.txt
# vim survival: i to insert, Esc, :wq to save+quit

# search + pipes + redirection
grep -i "error" /var/log/syslog
grep -rn "listen" /etc/nginx/
cat /etc/passwd | grep bash | wc -l
ls -l /etc > etc-listing.txt
echo "deploy done" >> deploy.log
```

## 3. 🏢 Real production example
`tail -f` on an app log while you reproduce a bug; `grep -i error` to jump straight to the failure line. This is 80% of on-call triage.

## 4. 📝 Exercise / challenge
- Given a log file, use `grep` + `wc -l` to count errors, and `tail -f` to watch it live while you append lines from another terminal.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `tail -f file` | Follow a file live |
| `grep -rin "text" dir/` | Recursive, case-insensitive, line numbers |
| `cmd | grep x` | Filter output |
| `cmd > file` / `>>` | Overwrite / append to file |

## 6. 🎯 Next-lesson preview
→ **Video 04: Text Processing** — turn raw output into exactly the data you want with `awk` and `sed`.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Read & Edit Files in Linux (cat, grep, vim, pipes)
- **Primary keyword:** linux grep tutorial
- **Thumbnail idea:** Terminal with a `grep -i error` line glowing red
- **Shorts to cut:** "tail -f will save your on-call shift" · "vim: just get out (i, Esc, :wq)"
