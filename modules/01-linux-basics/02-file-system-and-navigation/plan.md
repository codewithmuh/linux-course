# Video 02 — Linux File System & Navigation

**Module 1 · Linux Basics · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Everything in Linux is a file. Learn this one tree and you'll never feel lost on a server again."

## What you'll learn
- The Linux directory structure (`/`, `/etc`, `/var`, `/home`, `/tmp`, `/usr`, `/bin`)
- Where you are and how to move: `pwd`, `ls`, `cd`
- Create things: `mkdir`, `touch`
- Move and remove things: `cp`, `mv`, `rm`
- Find anything: `find`

## 1. 🎨 Animated slides (3–5 min)
- The filesystem hierarchy as a tree — what lives where and why
- Absolute vs relative paths (`/`, `.`, `..`, `~`)
- What "everything is a file" means

## 2. 💻 Hands-on demo (10–15 min)
```bash
pwd
ls -lah
cd /var/log && ls
cd ~            # home
mkdir -p projects/app/logs
touch projects/app/README.md
cp projects/app/README.md /tmp/
mv /tmp/README.md /tmp/notes.md
rm /tmp/notes.md
find / -name "*.log" -type f 2>/dev/null | head
find . -type d
```

## 3. 🏢 Real production example
Debugging a service: `cd /etc/nginx`, inspect config; `cd /var/log/nginx`, read the access/error logs. Knowing where things live *is* the job.

## 4. 📝 Exercise / challenge
- Recreate a small project tree with `mkdir -p`, then use `find` to list only the directories, then only files modified today.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `pwd` | Where am I |
| `ls -lah` | List, long + hidden + human sizes |
| `cd -` | Jump back to previous dir |
| `mkdir -p a/b/c` | Create nested dirs |
| `find . -name "*.log"` | Find files by name |

## 6. 🎯 Next-lesson preview
→ **Video 03: Working with Files** — now that you can move around, learn to read and edit what's inside.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** The Linux File System Explained (Navigate Like a Pro)
- **Primary keyword:** linux file system explained
- **Thumbnail idea:** Directory tree diagram with `/etc /var /home` highlighted
- **Shorts to cut:** "The Linux directory tree in 60s" · "find, the command you'll use forever"
