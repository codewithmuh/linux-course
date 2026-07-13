# Bash Basics

> [Linux for DevOps](../../README.md) · Module 4 — Bash Scripting

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- The shebang, making a script executable, and running it
- Variables and command substitution
- Reading input and printing output
- Conditions (`if`, `test`, `[[ ]]`)
- Loops (`for` and `while`)

## Concepts

A **shell script** is just a file full of the commands you'd otherwise type by hand. The first line — the **shebang** `#!/usr/bin/env bash` — tells the system which interpreter should run the file.

**Variables** hold values (`name="Rashid"`) and you read them back with `$name`. Wrap expansions in quotes (`"$name"`) so spaces don't break things. **Command substitution** `$(...)` captures the output of a command, e.g. `today=$(date +%F)`.

Bash conditions run on **exit codes**, not the words `true`/`false`: a command that exits `0` counts as success (truthy), anything else is failure. That's what drives `if`.

## Commands

```bash
# The full script lives in scripts/hello.sh — here's the shape of it:

name="${1:-}"                    # first argument, or empty
if [[ -z "$name" ]]; then        # if it's empty...
  read -rp "Your name: " name    # ...ask for it
fi
echo "Hello, $name — today is $(date +%F)"   # command substitution

for i in 1 2 3; do               # loop over a list
  echo "count $i"
done

count=0
while [[ $count -lt 3 ]]; do     # loop while a condition holds
  echo "while $count"
  count=$((count + 1))
done
```

Make it executable and run it:

```bash
chmod +x hello.sh
./hello.sh            # prompts for your name
./hello.sh Rashid     # takes the name as an argument
```

## What the names mean

| Name | Stands for |
|---|---|
| `bash` | **B**ourne **A**gain **SH**ell — a pun: the original shell was written by Steve Bourne |
| shebang `#!` | "sharp" (`#`) + "bang" (`!`) |
| `echo` | prints back what you give it — like an echo |
| `read` | reads what the user types |

## In production
Your very first useful script is a tiny status checker: it asks whether a service is running and prints a clear answer. That pattern — check something, report it plainly — is the seed of every health-check and bootstrap script you'll write later.

## Practice
- Write a script that takes a directory as an argument and prints how many files it contains. If no directory is given, default to the current directory.

## Cheat sheet
| Syntax | Meaning |
|---|---|
| `#!/usr/bin/env bash` | Shebang |
| `var="value"` / `$var` | Set / use a variable |
| `$(cmd)` | Command substitution |
| `if [[ cond ]]; then … fi` | Condition |
| `for x in …; do … done` | Loop |

## Scripts
- [`scripts/hello.sh`](scripts/hello.sh) — greeting script showing variables, input, conditions, and both loop styles.

---
← [Course home](../../README.md) · **Next:** [Advanced Bash](../14-advanced-bash/README.md)
