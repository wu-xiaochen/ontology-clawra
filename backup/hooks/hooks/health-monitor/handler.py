import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

HOOKS_DIR = Path(__file__).parent
LOG_FILE = HOOKS_DIR / "health.log"
STATE_FILE = HOOKS_DIR / "state.json"


def log(msg: str):
    timestamp = datetime.now().isoformat()
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def send_telegram_alert(message: str):
    """Send alert via Hermes MCP - the cron job will deliver to Telegram."""
    # We just log it - the cron delivery system handles Telegram
    log(f"ALERT: {message}")


def handle_event(event: dict, context: dict):
    """
    Handle gateway hook events.
    event.type tells us what happened.
    """
    event_type = event.get("type", "unknown")
    payload = event.get("payload", {})

    if event_type == "gateway:start":
        log("Gateway started - agent is online")
        # Don't alert on normal start

    elif event_type == "cron:failed":
        job_name = payload.get("job_name", "unknown")
        job_id = payload.get("job_id", "unknown")
        error = payload.get("error", "unknown error")
        log(f"Cron FAILED: {job_name} ({job_id}) - {error}")
        send_telegram_alert(f"⚠️ Cron任务失败: {job_name}\n错误: {error}")

    elif event_type == "cron:completed":
        job_name = payload.get("job_name", "unknown")
        job_id = payload.get("job_id", "unknown")
        # Only log, don't alert - success is silent
        log(f"Cron OK: {job_name} ({job_id})")

    elif event_type == "agent:error":
        error_msg = payload.get("error", "unknown")
        log(f"Agent error: {error_msg}")
        # Alert for agent errors
        send_telegram_alert(f"🤖 Agent错误: {error_msg}")

    else:
        log(f"Unhandled event type: {event_type}")


if __name__ == "__main__":
    try:
        event = json.loads(sys.stdin.read())
        context = {}
        handle_event(event, context)
    except Exception as e:
        log(f"Hook error: {e}\n{traceback.format_exc()}")
        sys.exit(1)
