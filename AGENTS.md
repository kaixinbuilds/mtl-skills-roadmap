# Working agreement: Claude Code and Codex

Both agents work on this repo for the HOD/MTL (Mdm Chun Kai Xin). Codex reads this file on its own; Claude reads it through `CLAUDE.md`. Read `HANDOFF.md` for what the site is and how it is built before changing anything.

## Roles

- **Claude Code: builder.** Owns `index.html`, `tools/*.py` and `tools/*.json`, and `HANDOFF.md`. Makes the changes and regenerates the page.
- **Codex: reviewer and graphics.** Reviews Claude's changes and the live page. Makes graphics (SVG first, PNG only for raster art) in `assets/`. Codex does not edit `index.html` or `tools/`. It proposes changes in the thread, and may attach a patch file under `collab/patches/`.
- **HOD: decides.** Anything about syllabus facts, school policy or what goes public is the HOD's decision. Either agent marks such a point `NEEDS HOD` in the thread instead of guessing. Claims about MOE or SEAB documents must cite the source, as the HOD expects.

## How we talk: `collab/threads/`

All agent-to-agent messages go in one Markdown file per topic under `collab/threads/`, named `YYYY-MM-DD-short-topic.md`. Nothing is passed through the HOD.

Each thread starts with this header:

```
---
topic: Review of course map summary layout
kind: review | graphics | question
to: codex | claude
status: open | answered | closed
---
```

- Write the request under `## Request (Claude, 31 Oct 2026)` or `## Request (Codex, ...)`. Say what to look at (files, commit, tab and width), what done looks like, and where output goes.
- Reply by appending `## Reply (Codex, date)` or `## Reply (Claude, date)`. Never edit the other agent's sections.
- When you reply, set `to:` to the other agent and `status: answered`. The agent that opened the thread sets `status: closed` once it has acted on the reply.
- Review replies list findings most important first. Each finding gives the file and line, or the tab and width, what is wrong and the fix. Label each **Must fix**, **Should fix** or **Idea**.
- Graphics replies list each file in `assets/`, its size, where it is meant to go and its alt text. Every SVG must work on the light and dark backgrounds the page uses, have a `viewBox` and no external fonts or images, and keep the CL, ML and TL text exactly as given in the request.

**At the start of every session, and whenever the HOD says "check collab"**, list `collab/threads/` and deal with every thread whose header has `to:` set to you and `status` either `open` (a request to act on) or `answered` (a reply to act on, then close), before other work. Mention them to the HOD.

## Waking the other agent

Either agent can run the other in the background on this repo:

- Claude runs `tools/collab/ask-codex.sh collab/threads/<file>.md`
- Codex runs `tools/collab/ask-claude.sh collab/threads/<file>.md`

The script tells the other agent to handle that thread and append its reply. Rules:

- Only wake the other agent for a thread you just opened or updated. If the script was what started you (`COLLAB_CALLED_BY` is set), do not wake the other agent again: reply in the thread and stop. This stops the two agents from waking each other in a loop.
- One writer at a time. While the other agent is working, do not edit the files it may touch.
- The other agent's CLI needs network access and writes its own state outside the repo, so a sandboxed agent must ask the HOD to approve running the script outside the sandbox. Codex: request escalation for that one command.
- If the script fails (not signed in, sandbox, network), tell the HOD and leave the thread as it was: a new request stays `open`, a reply already given stays `answered`. The HOD can then say "check collab" to the other agent.

## Git

- Commit your own work with a clear message. Commit the thread file together with the work it is about.
- Do not push, merge or open PRs unless the HOD asks for it in that conversation. The `HANDOFF.md` and Claude's notes record how pushing works from this Mac.
- Never rewrite history or discard the other agent's uncommitted work.
