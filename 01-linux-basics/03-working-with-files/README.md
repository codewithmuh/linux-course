# Working with Files

> [Linux for DevOps](../../README.md) · Module 1 — Linux Basics

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- View files: `cat`, `less`, `head`, `tail` (incl. `tail -f`)
- Edit files: `nano` and `vim` survival basics
- Search inside files: `grep`
- Chain commands: pipes `|` and redirection `>`, `>>`, `<`

## Concepts

Every command has three streams: **stdin** (input), **stdout** (normal output), and **stderr** (errors). A **pipe** `|` feeds one command's stdout into the next's stdin. **Redirection** sends a stream to (or from) a file.

```mermaid
flowchart LR
  A[cat access.log] -->|pipe| B[grep error] -->|pipe| C[wc -l]
  C --> D["> errors.count"]
```

## Commands
```bash
cat /etc/os-release
less /var/log/syslog          # q to quit; / to search
head -n 20 /var/log/syslog
tail -n 20 /var/log/syslog
tail -f /var/log/syslog       # follow live (Ctrl-C to stop)

# edit
nano notes.txt                # beginner-friendly
# vim survival: press i to insert, Esc to stop, :wq to save+quit

# search + pipes + redirection
grep -i "error" /var/log/syslog
grep -rn "listen" /etc/nginx/         # recursive, with line numbers
cat /etc/passwd | grep bash | wc -l   # count bash users
ls -l /etc > etc-listing.txt          # overwrite a file
echo "deploy done" >> deploy.log      # append to a file
```

## In production
`tail -f` an application log while you reproduce a bug, then `grep -i error` to jump straight to the failing line. That combination is how most production problems get found.

## Practice
- Given a log file, use `grep` + `wc -l` to count the errors.
- Use `tail -f` to watch a file live while you append lines to it from a second terminal.

## Cheat sheet
| Command | What it does |
|---|---|
| `tail -f file` | Follow a file live |
| `grep -rin "text" dir/` | Recursive, case-insensitive, line numbers |
| `cmd \| grep x` | Filter output |
| `cmd > file` / `>>` | Overwrite / append to file |
| `less file` | Page through a file |

---
← [Course home](../../README.md) · **Next:** [Text Processing](../04-text-processing/README.md)
