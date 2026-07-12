# Video 13 — Bash Basics

**Module 4 · Bash Scripting · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "If you've typed the same three commands twice today, you should've scripted them. Let's write your first Bash script — right now."

## What you'll learn
- Shebang, making a script executable, running it
- Variables and command substitution
- Reading input, printing output
- Conditions (`if`, `test`, `[[ ]]`)
- Loops (`for`, `while`)

## 1. 🎨 Animated slides (3–5 min)
- What a shell script is (a file of commands)
- The shebang `#!/usr/bin/env bash`
- Variables, quoting, and `$(...)` command substitution
- Truthiness: exit codes drive `if`

## 2. 💻 Hands-on demo (10–15 min)
```bash
cat > hello.sh <<'EOF'
#!/usr/bin/env bash
name="$1"
if [[ -z "$name" ]]; then
  read -rp "Your name: " name
fi
echo "Hello, $name — today is $(date +%F)"

for i in 1 2 3; do
  echo "count $i"
done

count=0
while [[ $count -lt 3 ]]; do
  echo "while $count"
  ((count++))
done
EOF

chmod +x hello.sh
./hello.sh
./hello.sh Rashid
```

## 3. 🏢 Real production example
A tiny script that checks whether a service is running and prints a clear status — the seed of every health-check and bootstrap script you'll write later.

## 4. 📝 Exercise / challenge
- Write a script that takes a directory as an argument and prints how many files it contains, defaulting to the current directory if none is given.

## 5. 📄 Cheat sheet (downloadable)
| Syntax | Meaning |
|---|---|
| `#!/usr/bin/env bash` | Shebang |
| `var="value"` / `$var` | Set / use variable |
| `$(cmd)` | Command substitution |
| `if [[ cond ]]; then … fi` | Condition |
| `for x in …; do … done` | Loop |

## 6. 🎯 Next-lesson preview
→ **Video 14: Advanced Bash** — functions, arrays, arguments, and the error handling that makes scripts production-safe.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Bash Scripting for Beginners (Your First Script)
- **Primary keyword:** bash scripting tutorial
- **Thumbnail idea:** `#!/bin/bash` with a "your first script" badge
- **Shorts to cut:** "Your first Bash script in 60 seconds" · "if statements in Bash, explained"
