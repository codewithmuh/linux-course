# Linux for DevOps — Course Repo (devopsbymuh)

The complete **Linux & Bash** course for the [devopsbymuh](https://youtube.com/@codewithmuh) channel — tool #1 in the DevOps learning roadmap. This repo holds the production plan, demos, scripts, and cheat sheets for the whole course.

**18 exceptional videos > 30 average videos.** Every video is planned to feel premium and to leave the viewer with a real, usable skill.

## The premium video format

Every video follows the same six-part shape:

| Part | Length | What it is |
|---|---|---|
| 🎨 Animated slides | 3–5 min | Clean motion-graphic concept explanation |
| 💻 Hands-on demo | 10–15 min | Real terminal, run every command live |
| 🏢 Production example | — | How this is actually used on the job |
| 📝 Exercise / challenge | — | Viewer does it themselves |
| 📄 Cheat sheet | — | Optional downloadable reference |
| 🎯 Next-lesson preview | — | Hook into the following video |

Target length per video: **~18–20 min**.

## Course map (5 modules · 18 videos)

| Module | Videos | Folder |
|---|---|---|
| 1 · Linux Basics | 01–04 | [`modules/01-linux-basics`](modules/01-linux-basics) |
| 2 · Linux Administration | 05–09 | [`modules/02-linux-administration`](modules/02-linux-administration) |
| 3 · Networking | 10–12 | [`modules/03-networking`](modules/03-networking) |
| 4 · Bash Scripting | 13–15 | [`modules/04-bash-scripting`](modules/04-bash-scripting) |
| 5 · Linux for DevOps | 16–18 | [`modules/05-linux-for-devops`](modules/05-linux-for-devops) |

The course ends with a **capstone**: deploy a production Linux server (video 18) using everything learned.

## Repo structure

```
modules/
  NN-module-name/
    README.md               Module goal + video list
    NN-video-slug/
      plan.md               Production plan (premium 6-part format)  ← start here
      demo/                 Scripts/files used in the live demo (added when producing)
      cheatsheet.md         Downloadable reference (added when producing)
_templates/
  video-plan.md             Copy this to start a new video plan
```

## Producing a video

1. Open the video's `plan.md` (already seeded with topics + the premium format).
2. Flesh out the slides outline and the exact demo commands.
3. Drop demo scripts into that video's `demo/` folder.
4. Write the `cheatsheet.md`.
5. Generate packaging (title, thumbnail, description, shorts) — the `/yt-*` skills in the planning workspace, rebranded to **devopsbymuh**.

## Related

Channel strategy + full tool roadmap live in the planning workspace repo `~/youtube-devopsbymuh` (`channel/strategy.md`, `channel/learning-roadmap.md`). This Linux course is the first course of Phase 1.
