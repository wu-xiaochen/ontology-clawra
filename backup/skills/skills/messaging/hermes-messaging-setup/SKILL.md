---
name: hermes-messaging-setup
description: Configure WhatsApp and Telegram messaging platforms on Hermes Agent
---
# Hermes Agent Messaging Platforms Setup

## Key Discovery
**Hermes Agent uses TWO separate config systems:**
- `~/.hermes/config.yaml` — general agent config
- `~/.hermes/.env` — messaging platforms, API keys, credentials

**Messaging platforms (WhatsApp, Telegram, Discord, etc.) MUST be configured via `.env`**, NOT `config.yaml`. Use `hermes config set` command, never edit `.env` directly.

## WhatsApp Setup

### Config in ~/.hermes/.env:
```bash
WHATSAPP_MODE=bot
WHATSAPP_ALLOWED_USERS=13920378337   # International format, no + sign
```

### Important: WhatsApp Personal Account Limitation
- WhatsApp personal account connected via QR code becomes the bot
- **Cannot** message yourself to test — WhatsApp doesn't relay self-messages to the bot
- Need another person to message your number, OR use WhatsApp Business as a separate bot account
- `Channel directory built: 0 target(s)` = no active sessions yet

### If bridge keeps disconnecting:
- This is a known Baileys bridge issue with WhatsApp personal accounts
- Try `hermes whatsapp` to re-pair if session was invalidated

## Telegram Setup

### Step 1: Create bot via @BotFather
1. Message @BotFather on Telegram
2. Send `/newbot`, follow prompts
3. Copy the bot token (format: `123456789:ABCdef...`)

### Step 2: Get your Telegram User ID
1. Search @userinfobot on Telegram
2. Send any message — it replies with your numeric User ID

### Step 3: Configure Hermes (in ~/.hermes/.env)
```bash
hermes config set TELEGRAM_BOT_TOKEN "123456789:ABCdef..."
hermes config set TELEGRAM_ALLOWED_USERS "123456789"  # Your Telegram user ID, NOT phone number
```

### Step 4: Restart gateway
```bash
hermes gateway restart
```

### Step 5: Verify
Check logs: `tail -20 ~/.hermes/logs/gateway.log`
Should see: `✓ telegram connected`

## macOS + SOCKS Proxy (China Firewall)

If Telegram fails with `httpx.ConnectError` or `NetworkError`:

1. Check if you have a SOCKS proxy running:
```bash
networksetup -getsocksfirewallproxy Wi-Fi
```

2. If proxy exists (e.g., ClashX at 127.0.0.1:7897), set env vars:
```bash
launchctl setenv HTTP_PROXY socks5://127.0.0.1:7897
launchctl setenv HTTPS_PROXY socks5://127.0.0.1:7897
```

3. Install socksio for httpx:
```bash
uv pip install httpx[socks] --python ~/.hermes/hermes-agent/venv/bin/python
```

4. Restart gateway:
```bash
hermes gateway restart
```

Note: Common proxy port is 7890 (Clash) or 7897 (ClashX), not 1080.

## Common Issues

### approvals.mode: manual
- All messages require manual approval — bot won't respond
- Fix: `hermes config set approvals.mode auto`

### Channel directory built: 0 target(s)
- No active messaging sessions yet
- For WhatsApp: need someone to send a message to your number
- For Telegram: need to message the bot from your account

### Gateway not picking up new config
- Always run `hermes gateway restart` after config changes

## Verification Commands
```bash
hermes gateway status        # Check gateway and platform status
tail -20 ~/.hermes/logs/gateway.log  # View recent logs
```
