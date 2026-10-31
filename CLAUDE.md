@AGENTS.md

## Claude-specific notes

- Codex CLI on this Mac: `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex` (bundled with the ChatGPT app, not on PATH). `tools/collab/ask-codex.sh` finds it.
- `ask-codex.sh` can run for several minutes. Run it in the background and read the thread file when it finishes.
- Verification without `node`: use `jsc` for syntax checks and a python `http.server` preview in the built-in browser.
