# Linux File System & Navigation

> [Linux for DevOps](../../README.md) · Module 1 — Linux Basics

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- The Linux directory structure
- Where you are and how to move: `pwd`, `ls`, `cd`
- Create things: `mkdir`, `touch`
- Copy, move, remove: `cp`, `mv`, `rm`
- Find anything: `find`

## Concepts

In Linux **everything hangs off a single root, `/`** — there are no drive letters. Learn this tree once and you'll never feel lost on a server.

```mermaid
flowchart TB
  root["/"]
  root --> etc["/etc — config"]
  root --> var["/var — logs, variable data"]
  root --> home["/home — user files"]
  root --> usr["/usr — installed software"]
  root --> tmp["/tmp — temporary files"]
  root --> bin["/bin — core commands"]
```

**Paths** are either **absolute** (start at `/`, e.g. `/var/log/nginx`) or **relative** (from where you are). Handy shortcuts: `.` = here, `..` = up one, `~` = your home.

## Commands
```bash
pwd                      # pwd = "print working directory" — where am I
ls -lah                  # ls = "list": long + hidden + human sizes
cd /var/log && ls        # cd = "change directory"
cd ~                     # home
cd -                     # jump back to previous dir

mkdir -p projects/app/logs        # mkdir = "make directory" (-p: parents too)
touch projects/app/README.md      # create an empty file (or update its date)
cp projects/app/README.md /tmp/   # cp = "copy"
mv /tmp/README.md /tmp/notes.md   # mv = "move" — also how you rename
rm /tmp/notes.md                  # rm = "remove"

find / -name "*.log" -type f 2>/dev/null | head
find . -type d                    # only directories
find . -mtime -1                  # changed in the last day
```

## What the names mean
Commands:

| Command | Stands for |
|---|---|
| `pwd` | **p**rint **w**orking **d**irectory |
| `ls` | **l**i**s**t |
| `cd` | **c**hange **d**irectory |
| `mkdir` | **m**a**k**e **dir**ectory |
| `cp` / `mv` / `rm` | **c**o**p**y / **m**o**v**e / **r**e**m**ove |
| `touch` | not an abbreviation — it "touches" a file: creates it empty, or updates its date |

And the folder names:

| Folder | Stands for |
|---|---|
| `/etc` | "et cetera" (an old name) — today it means: system config files |
| `/var` | **var**iable data — files that grow, like logs |
| `/usr` | **U**nix **s**ystem **r**esources — installed software |
| `/tmp` | **t**e**mp**orary files |
| `/bin` | **bin**aries — the programs themselves |

## In production
Debugging a service is mostly navigation: `cd /etc/nginx` to read the config, `cd /var/log/nginx` to read the logs. Knowing **where things live** is half the job.

## Practice
- Recreate a small project tree with `mkdir -p`.
- Use `find` to list only the directories, then only files modified today.

## Cheat sheet
| Command | What it does |
|---|---|
| `pwd` | Where am I |
| `ls -lah` | List long + hidden + sizes |
| `cd -` | Back to previous dir |
| `mkdir -p a/b/c` | Create nested dirs |
| `find . -name "*.log"` | Find files by name |

---
← [Course home](../../README.md) · **Next:** [Working with Files](../03-working-with-files/README.md)
