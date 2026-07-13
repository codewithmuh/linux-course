# Text Processing

> [Linux for DevOps](../../README.md) · Module 1 — Linux Basics

> 📺 **Watch:** _video link coming soon_

## What you'll learn
- Reshape data: `sort`, `uniq`, `cut`, `paste`, `wc`
- Field extraction and reporting with `awk`
- Find-and-replace and stream editing with `sed`

## Concepts

Unix tools see text as **lines** made of **fields**. Chain small tools into a pipeline and you can answer real questions — like "which 10 IP addresses send my server the most requests?" — in one line.

- **`cut`** — grab specific fields
- **`sort | uniq -c | sort -rn`** — rank things by frequency
- **`awk`** — fields, filters, and math
- **`sed`** — find-and-replace / stream editing

## Commands
```bash
# counting + ranking   (uniq = "unique", wc = "word count")
cut -d: -f1 /etc/passwd | sort | uniq | wc -l   # how many different users?
sort access.log | uniq -c | sort -rn | head     # rank lines by how often they appear

# cut / paste
cut -d, -f1,3 data.csv           # take columns 1 + 3 (-d, = split on commas)
paste names.txt scores.txt       # join two files side by side

# awk: fields, filters, sums   (named after its creators: Aho, Weinberger, Kernighan)
awk -F: '{print $1}' /etc/passwd                # print field 1 (-F: = split on colons)
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head   # top IPs
awk -F: '$3 >= 1000 {print $1}' /etc/passwd                       # real users

# sed = "stream editor": substitution + in-place edit
sed 's/error/ERROR/g' app.log                   # replace error → ERROR (g = every match)
sed -i 's/localhost/127.0.0.1/g' config.ini     # -i = change the file itself
sed -n '10,20p' file.txt                                          # print a line range
```

## What the names mean

| Command | Stands for |
|---|---|
| `wc` | **w**ord **c**ount |
| `uniq` | **uniq**ue |
| `sed` | **s**tream **ed**itor |
| `awk` | the initials of its three creators: **A**ho, **W**einberger, **K**ernighan |
| `cut` / `sort` / `paste` | plain English — they do exactly what they say |

## In production
Parse an Nginx access log to find the top 10 client IPs and the most-requested URLs — a one-liner that answers "where is all this traffic coming from?" in seconds, with no extra tools.

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
