# Video 04 — Text Processing

**Module 1 · Linux Basics · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "Give me a messy log file and one line of `awk`, and I'll give you the top 10 IPs hitting your server. Text processing is a superpower."

## What you'll learn
- Reshape data: `sort`, `uniq`, `cut`, `paste`, `wc`
- Field extraction and reporting with `awk`
- Find-and-replace and stream editing with `sed`

## 1. 🎨 Animated slides (3–5 min)
- Lines and fields — how Unix tools see text
- The pipeline as an assembly line (`sort | uniq -c | sort -rn`)
- When to reach for `awk` vs `sed` vs `cut`

## 2. 💻 Hands-on demo (10–15 min)
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
sed -n '10,20p' file.txt                                          # print a range
```

## 3. 🏢 Real production example
Parse an Nginx access log to find the top 10 client IPs and the most-requested URLs — a one-liner that answers "who's hammering us?" in seconds.

## 4. 📝 Exercise / challenge
- From a sample access log, produce a ranked table of the top 10 IPs, then rewrite all `404` lines to be tagged `NOTFOUND` with `sed`.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `sort | uniq -c | sort -rn` | Rank by frequency |
| `awk -F: '{print $1}'` | Print field 1, `:`-delimited |
| `awk '$3>1000'` | Filter rows by a field condition |
| `sed 's/a/b/g'` | Replace all `a` with `b` |
| `sed -i` | Edit the file in place |

## 6. 🎯 Next-lesson preview
→ **Video 05: Users & Groups** — Module 2 begins. Time to administer the system, starting with who's allowed on it.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** awk & sed for DevOps (Text Processing You'll Actually Use)
- **Primary keyword:** awk sed tutorial linux
- **Thumbnail idea:** Messy log → clean ranked table, arrow between them
- **Shorts to cut:** "Top 10 IPs with one line of awk" · "sed find-and-replace across a file"
