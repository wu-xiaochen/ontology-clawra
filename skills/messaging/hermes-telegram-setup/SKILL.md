---
name: hermes-telegram-setup
description: Configure Telegram bot messaging channel for Hermes Agent, especially useful when behind Chinese firewall with SOCKS proxy
triggers:
  - "configure telegram"
  - "setup telegram on hermes"
  - "telegram bot hermes agent"
  - "hermes telegram behind firewall"
---

# Hermes Agent + Telegram Setup (Chinese Firewall / SOCKS Proxy)

## Prerequisites
- Telegram Bot Token from @BotFather
- Your Telegram User ID from @userinfobot
- VPN with SOCKS proxy (typically 127.0.0.1:7897)

## Step 1: Get Credentials
1. Message **@BotFather** → `/newbot` → copy token (format: `123456789:ABC...`)
2. Message **@userinfobot** → copy your **User ID** (numeric)

## Step 2: Configure Hermes
```bash
# Set bot token
hermes config set TELEGRAM_BOT_TOKEN "your_token_here"

# Set allowed user (your User ID)
hermes config set TELEGRAM_ALLOWED_USERS your_user_id

# Approvals must be auto (not manual) or messages get blocked
# Check: grep "approvals" ~/.hermes/config.yaml → mode: auto
```

## Step 3: Install SOCKS Support (Required for Chinese firewall)
```bash
uv pip install httpx[socks] --python ~/.hermes/hermes-agent/venv/bin/python
```

## Step 4: Restart Gateway
```bash
hermes gateway restart
```

## Step 5: Verify Connection
```bash
tail -20 ~/.hermes/logs/gateway.log
# Look for: [Telegram] Connected to Telegram (polling mode)
```

## Sending Files via Telegram API (CLI)
When sending photos/files via curl to Telegram API, you MUST use the proxy:
```bash
HTTP_PROXY=socks5://127.0.0.1:7897 HTTPS_PROXY=socks5://127.0.0.1:7897 \
  curl -s --max-time 60 -X POST \
  "https://api.telegram.org/bot<TOKEN>/sendPhoto" \
  -F "chat_id=your_user_id" \
  -F "photo=@/path/to/image.png"
```

## Troubleshooting

**curl still times out**: Your VPN's SOCKS proxy port may differ — check with:
```bash
networksetup -getsocksfirewallproxy Wi-Fi
# Returns: Server: 127.0.0.1, Port: XXXX
```

**Telegram connect fails repeatedly**: Check `~/.hermes/logs/gateway.log` — if you see `NetworkError: httpx.ConnectError`, the SOCKS package is missing (see Step 3)

**Messages not replied to**: Check `approvals.mode` in config — must be `auto`, not `manual`

**WhatsApp bridge crashes constantly**: Known issue with WhatsApp Bridge (Baileys). Use Telegram instead — it's more stable behind Chinese firewall.

## Key Differences from OpenClaw
- Config file: `~/.hermes/config.yaml` (NOT `openclaw.json`)
- Secrets/Tokens: `~/.hermes/.env` (NOT in config.yaml)
- Messaging channels: configured via `.env` and `config.yaml`, not a separate setup wizard
