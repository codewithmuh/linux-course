#!/usr/bin/env bash
# hello.sh — your first Bash script: variables, input, conditions, and loops.
# Usage: ./hello.sh [name]
#   Pass a name as the first argument, or you'll be prompted for one.
set -euo pipefail

# Variable + a default so `set -u` doesn't error when no argument is passed.
name="${1:-}"

# Condition: if the name is empty, read one from standard input.
if [[ -z "$name" ]]; then
  read -rp "Your name: " name
fi

# Command substitution: $(date +%F) is replaced by today's date.
echo "Hello, $name — today is $(date +%F)"

# for loop over a fixed list.
for i in 1 2 3; do
  echo "count $i"
done

# while loop with a counter.
count=0
while [[ $count -lt 3 ]]; do
  echo "while $count"
  count=$((count + 1))   # avoids the ((count++)) exit-code trap under `set -e`
done
