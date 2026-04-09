#!/bin/bash
# install.sh — install skill-vetter and its dependencies
# Usage:
#   bash install.sh                    (from cloned repo)
#   bash <(curl -s https://raw.githubusercontent.com/app-incubator-xyz/skill-vetter/master/scripts/install.sh)

set -euo pipefail

REPO_URL="https://github.com/app-incubator-xyz/skill-vetter.git"
SKILL_NAME="skill-vetter"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Skill Vetter — Installer"
echo "════════════════════════════════════════════════════════════"
echo ""

# ── Detect OS ────────────────────────────────────────────────────────────────

OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux"* ]]; then
    OS="linux"
fi

# ── Install prerequisites ────────────────────────────────────────────────────

installed=()
skipped=()

echo "▸ Checking prerequisites..."
echo ""

# jq
if command -v jq &>/dev/null; then
    echo "  ✅ jq"
else
    echo "  ⏳ Installing jq..."
    if [[ "$OS" == "macos" ]] && command -v brew &>/dev/null; then
        brew install jq -q
        installed+=("jq")
    elif [[ "$OS" == "linux" ]] && command -v apt &>/dev/null; then
        sudo apt install -y jq -qq
        installed+=("jq")
    else
        echo "  ⚠️  Could not install jq automatically"
        skipped+=("jq")
    fi
fi

# aguara
if command -v aguara &>/dev/null; then
    echo "  ✅ aguara"
else
    echo "  ⚠️  aguara not installed"
    echo "     See: https://github.com/garagon/aguara"
    skipped+=("aguara")
fi

# skill-scanner
if command -v skill-scanner &>/dev/null; then
    echo "  ✅ skill-scanner"
else
    echo "  ⚠️  skill-scanner not installed"
    echo "     See: https://pypi.org/project/cisco-ai-skill-scanner/"
    skipped+=("skill-scanner")
fi

# git, curl — just check, don't try to install
for tool in git curl; do
    if command -v "$tool" &>/dev/null; then
        echo "  ✅ $tool"
    else
        echo "  ❌ $tool — please install manually"
        skipped+=("$tool")
    fi
done

echo ""

# ── Get the skill source ────────────────────────────────────────────────────

SKILL_SRC=""

# If SKILL.md exists in current or parent dir, we're inside the repo
if [[ -f "./SKILL.md" ]]; then
    SKILL_SRC="$(pwd)"
elif [[ -f "../SKILL.md" && -f "../scripts/vett.sh" ]]; then
    SKILL_SRC="$(cd .. && pwd)"
else
    # Clone from GitHub
    echo "▸ Cloning skill-vetter..."
    TMPDIR=$(mktemp -d)
    git clone --depth 1 "$REPO_URL" "$TMPDIR/$SKILL_NAME" 2>/dev/null
    SKILL_SRC="$TMPDIR/$SKILL_NAME"
fi

# ── Detect platform and install ─────────────────────────────────────────────

link_skill() {
    local target="$1"
    local dir
    dir="$(dirname "$target")"

    if [[ -e "$target" ]]; then
        echo "  ↳ Already exists: $target"
        return 0
    fi

    mkdir -p "$dir"
    ln -s "$SKILL_SRC" "$target"
    echo "  ↳ Linked: $target → $SKILL_SRC"
}

echo "▸ Installing skill..."
echo ""

installed_to=()

# Claude Code
if [[ -d "$HOME/.claude" ]]; then
    echo "  Found Claude Code"
    link_skill "$HOME/.claude/skills/$SKILL_NAME"
    installed_to+=("Claude Code")
fi

# OpenClaw
if [[ -d "$HOME/.openclaw" ]]; then
    echo "  Found OpenClaw"
    link_skill "$HOME/.openclaw/skills/$SKILL_NAME"
    installed_to+=("OpenClaw")
fi

# Neither found
if [[ ${#installed_to[@]} -eq 0 ]]; then
    echo "  No Claude Code or OpenClaw installation detected."
    echo ""
    echo "  Install manually:"
    echo "    Claude Code:  ln -s \"$SKILL_SRC\" ~/.claude/skills/$SKILL_NAME"
    echo "    OpenClaw:     ln -s \"$SKILL_SRC\" ~/.openclaw/skills/$SKILL_NAME"
fi

# ── Summary ──────────────────────────────────────────────────────────────────

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Done!"
echo ""

if [[ ${#installed_to[@]} -gt 0 ]]; then
    echo "  Installed to: ${installed_to[*]}"
fi
if [[ ${#installed[@]} -gt 0 ]]; then
    echo "  Prerequisites installed: ${installed[*]}"
fi
if [[ ${#skipped[@]} -gt 0 ]]; then
    echo "  Skipped (install manually): ${skipped[*]}"
fi

echo ""
echo "  Usage:  /skill-vetter <skill-name>"
echo "  Or:     bash $SKILL_SRC/scripts/vett.sh <skill-name>"
echo "════════════════════════════════════════════════════════════"
