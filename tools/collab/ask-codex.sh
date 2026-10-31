#!/bin/zsh
# Wake Codex on one collab thread. Usage: tools/collab/ask-codex.sh collab/threads/<file>.md
set -e
cd "$(dirname "$0")/../.."
thread="$1"
[[ -f "$thread" ]] || { echo "No such thread: $thread" >&2; exit 1; }
if [[ -n "$COLLAB_CALLED_BY" ]]; then echo "Started by $COLLAB_CALLED_BY; not waking Codex again." >&2; exit 1; fi
codex="${CODEX_BIN:-$(command -v codex 2>/dev/null || echo /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex)}"
[[ -x "$codex" ]] || { echo "Codex CLI not found; set CODEX_BIN." >&2; exit 1; }
mkdir -p collab/logs
log="collab/logs/$(basename "$thread" .md).codex.log"
COLLAB_CALLED_BY=claude "$codex" exec --sandbox workspace-write \
  -o "collab/logs/$(basename "$thread" .md).codex-last.txt" \
  "Claude has written to you in $thread. Read AGENTS.md and HANDOFF.md, do what the thread asks, and append your reply to $thread as AGENTS.md describes. COLLAB_CALLED_BY is set, so do not run ask-claude.sh. Do not commit or push." \
  > "$log" 2>&1 < /dev/null || { echo "Codex failed; see $log" >&2; exit 1; }
echo "Codex finished. Reply is in $thread"
