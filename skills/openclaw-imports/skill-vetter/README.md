# Skill Vetter

Multi-scanner security gate for AI agent skills. Run before installing any skill to Claude Code, OpenClaw, or your other favorite AI agent — whether from ClawHub, GitHub, or any external source.

## Installation

**One-liner** (installs prerequisites + skill):

```bash
bash <(curl -s https://raw.githubusercontent.com/app-incubator-xyz/skill-vetter/master/scripts/install.sh)
```

**Claude Code:**

```bash
git clone https://github.com/app-incubator-xyz/skill-vetter.git ~/.claude/skills/skill-vetter
```

**OpenClaw (via ClawHub):**

```bash
clawhub install skill-vetter
```

**From within a Claude Code session:**

> Ask Claude: "Install skill-vetter from https://github.com/app-incubator-xyz/skill-vetter"

Works out of the box with basic scanners (secrets + structure checks). Install `aguara` and `skill-scanner` for full coverage — run `bash scripts/check-deps.sh` to see what's missing.

## How to Run

### From terminal

```bash
bash scripts/vett.sh <skill-name | github-url | local-path>
```

### From an agent session

Type `/skill-vetter <name>` or ask the agent to scan a skill before installing it.

### As a Telegram slash command

Skill Vetter works as a Telegram slash command via OpenClaw's Telegram channel:

1. Create a bot via [@BotFather](https://t.me/BotFather) and copy the token
2. Configure OpenClaw with your bot token ([setup guide](https://docs.openclaw.ai/channels/telegram))
3. Start the OpenClaw gateway — skills with `user-invocable: true` auto-register as Telegram commands
4. Use `/skill_vetter <name>` in Telegram to scan a skill

> **Note:** Telegram command names only allow `[a-z0-9_]` — the hyphen in `skill-vetter` becomes an underscore automatically.

## Example Output

### SAFE

```
════════════════════════════════════════════════════════════
SKILL VETTER — Security Scan: youtube-watcher
════════════════════════════════════════════════════════════

[1/4] aguara............. ✅ PASS
[2/4] skill-scanner...... ✅ PASS
[3/4] secrets-scan....... ✅ PASS
[4/4] structure-check.... ✅ PASS

════════════════════════════════════════════════════════════
VERDICT: ✅ SAFE
All scanners passed
════════════════════════════════════════════════════════════
```

### BLOCKED

```
════════════════════════════════════════════════════════════
SKILL VETTER — Security Scan: totally-legit-helper
════════════════════════════════════════════════════════════

[1/4] aguara............. ❌ FAIL (prompt injection)
[2/4] skill-scanner...... ✅ PASS
[3/4] secrets-scan....... ❌ FAIL (credentials found)
[4/4] structure-check.... ❌ FAIL (curl|bash detected)

════════════════════════════════════════════════════════════
VERDICT: 🚫 BLOCKED
3 HIGH/CRITICAL findings
════════════════════════════════════════════════════════════
```

## Scanners

| Scanner | What It Checks |
|---------|----------------|
| [aguara](https://github.com/garagon/aguara) | Prompt injection, obfuscation, suspicious LLM calls |
| [skill-scanner](https://pypi.org/project/cisco-ai-skill-scanner/) | Known malicious patterns, CVE database |
| secrets-scan | Hardcoded API keys, tokens, credentials |
| structure-check | Missing SKILL.md, malformed YAML, dangerous shell commands |

## Verdicts

| Verdict | Action |
|---------|--------|
| **SAFE** | All scanners passed — proceed with installation |
| **REVIEW NEEDED** | Medium severity findings — review before deciding |
| **BLOCKED** | Critical/high findings — do not install |

## Dependencies

- [aguara](https://github.com/garagon/aguara) — prompt injection scanner
- [skill-scanner](https://pypi.org/project/cisco-ai-skill-scanner/) — Cisco AI vulnerability scanner
- `python3`, `curl`, `jq`, `git`

## License

MIT
