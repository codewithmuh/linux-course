# Text Processing

> [Linux for DevOps](../../README.md) · Module 1 — Linux Basics

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- Reshape data: `sort`, `uniq`, `cut`, `paste`, `wc`
- Field extraction and reporting with `awk`
- Find-and-replace and stream editing with `sed`

## Concepts

Unix tools see text as **lines** made of **fields**. Chain small tools into a pipeline and you can answer real questions — like "who are the top 10 IPs hitting my server?" — in one line.

- **`cut`** — grab specific fields
- **`sort | uniq -c | sort -rn`** — rank things by frequency
- **`awk`** — fields, filters, and math
- **`sed`** — find-and-replace / stream editing

## Commands
```bash
# counting + ranking
cut -d: -f1 /etc/passwd | sort | uniq | wc -l
sort access.log | uniq -c | sort -rn | head

# cut / paste
cut -d, -f1,3 data.csv
paste names.txt scores.txt

# awk: fields, filters, sums
awk -F: '{print $1}' /etc/passwd
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head   # top IPs
awk -F: '$3 >= 1000 {print $1}' /etc/passwd                       # real users

# sed: substitution + in-place edit
sed 's/error/ERROR/g' app.log
sed -i 's/localhost/127.0.0.1/g' config.ini
sed -n '10,20p' file.txt                                          # print a line range
```

## In production
Parse an Nginx access log to find the top 10 client IPs and the most-requested URLs — a one-liner that answers "who's hammering us?" in seconds, with no extra tooling.

## Practice
- From a sample access log, produce a ranked table of the top 10 IPs.
- Rewrite every `404` line to be tagged `NOTFOUND` using `sed`.

## Cheat sheet
| Command | What it does |
|---|---|
| `sort \| uniq -c \| sort -rn` | Rank by frequency |
| `awk -F: '{print $1}'` | Print field 1, `:`-delimited |
| `awk '$3>1000'` | Filter rows by a field condition |
| `sed 's/a/b/g'` | Replace all `a` with `b` |
| `sed -i` | Edit the file in place |

---
← [Course home](../../README.md) · **Next:** [Users & Groups](../../02-linux-administration/05-users-and-groups/README.md)
