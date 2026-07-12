# Video 06 — Linux Permissions

**Module 2 · Linux Administration · Target length: ~18–20 min**

> **Cold-open hook (first 20s):** "`Permission denied`. The error every beginner hates — and the one you'll never fear again after this video."

## What you'll learn
- Read a permission string (`-rwxr-xr--`) and the owner/group/other model
- Change permissions: `chmod` (symbolic + numeric)
- Change ownership: `chown`, `chgrp`
- Special bits: SUID, SGID, sticky bit

## 1. 🎨 Animated slides (3–5 min)
- Decode `-rwxr-xr--`: type, user, group, other
- Numeric permissions (4/2/1 → 755, 644, 600)
- What SUID/SGID/sticky actually do (and why `/tmp` is `1777`)

## 2. 💻 Hands-on demo (10–15 min)
```bash
ls -l script.sh
chmod +x script.sh
chmod 644 config.yaml
chmod 600 ~/.ssh/id_rsa          # private key must be locked down
chmod -R 755 /var/www/html

sudo chown deploy:deploy app.log
sudo chgrp webadmins /var/www

# special bits
ls -l /usr/bin/passwd            # note the SUID 's'
chmod g+s shared/                # SGID: new files inherit the group
ls -ld /tmp                      # sticky bit 't'
```

## 3. 🏢 Real production example
Why an app can't read its config, why an SSH key is rejected (`chmod 600`), and how a shared team directory uses SGID so everyone can collaborate on the files.

## 4. 📝 Exercise / challenge
- Make a script executable, lock a "secret" file to `600`, and set up a shared SGID directory where new files inherit the group.

## 5. 📄 Cheat sheet (downloadable)
| Command | What it does |
|---|---|
| `chmod +x f` | Make executable |
| `chmod 644 f` | rw-r--r-- |
| `chmod 600 f` | Owner-only (keys, secrets) |
| `chown u:g f` | Change owner + group |
| `chmod g+s dir` | SGID: inherit group |

## 6. 🎯 Next-lesson preview
→ **Video 07: Process Management** — files are under control; now let's control what's *running*.

## Packaging (fill later — use the /yt-* skills, rebrand to devopsbymuh)
- **Working title:** Linux Permissions Explained (chmod, chown, 644 vs 755)
- **Primary keyword:** linux permissions chmod explained
- **Thumbnail idea:** `-rwxr-xr--` broken into color-coded blocks
- **Shorts to cut:** "chmod numbers finally explained" · "Why your SSH key says Permission denied"
