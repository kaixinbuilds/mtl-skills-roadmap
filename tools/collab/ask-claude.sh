#!/bin/zsh
# Wake Claude Code on one collab thread. Usage: tools/collab/ask-claude.sh collab/threads/<file>.md
set -e
cd "$(dirname "$0")/../.."
thread="$1"
[[ -f "$thread" ]] || { echo "No such thread: $thread" >&2; exit 1; }
if [[ -n "$COLLAB_CALLED_BY" ]]; then echo "Started by $COLLAB_CALLED_BY; not waking Claude again." >&2; exit 1; fi
claude="${CLAUDE_BIN:-$(command -v claude || true)}"
if [[ -z "$claude" ]]; then
  # Claude desktop app bundles the CLI in a versioned folder; take the newest.
  claude=$(ls -d "$HOME/Library/Application Support/Claude/claude-code/"*/*/claude.app/Contents/MacOS/claude 2>/dev/null | sort -V | tail -1)
fi
[[ -x "$claude" ]] || { echo "Claude CLI not found; set CLAUDE_BIN." >&2; exit 1; }
mkdir -p collab/logs
log="collab/logs/$(basename "$thread" .md).claude.log"
COLLAB_CALLED_BY=codex "$claude" -p --permission-mode acceptEdits \
  --allowedTools "Read,Edit,Write,Glob,Grep,Bash(git status*),Bash(git diff*),Bash(git log*),Bash(python3 tools/*),Bash(jsc *)" \
  <<< "Codex has written to you in $thread. Do what the thread asks, and append your reply to $thread as AGENTS.md describes. COLLAB_CALLED_BY is set, so do not run ask-codex.sh. Do not push." \
  > "$log" 2>&1 || { echo "Claude failed; see $log" >&2; exit 1; }
echo "Claude finished. Reply is in $thread"
