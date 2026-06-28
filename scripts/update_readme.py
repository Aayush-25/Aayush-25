import re
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

README = Path(__file__).parent.parent / "README.md"
EVENTS_URL = "https://api.github.com/users/Aayush-25/events/public"


def time_ago(dt_str: str) -> str:
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    diff = int((datetime.now(timezone.utc) - dt).total_seconds())
    if diff < 60:
        return "just now"
    if diff < 3600:
        m = diff // 60
        return f"{m} minute{'s' if m != 1 else ''} ago"
    if diff < 86400:
        h = diff // 3600
        return f"{h} hour{'s' if h != 1 else ''} ago"
    if diff < 172800:
        return "yesterday"
    d = diff // 86400
    return f"{d} days ago"


def fetch_last_push() -> str | None:
    req = urllib.request.Request(
        EVENTS_URL,
        headers={
            "User-Agent": "readme-updater/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read().decode())
    except Exception as e:
        print(f"API error: {e}")
        return None

    event = next((e for e in events if e.get("type") == "PushEvent"), None)
    if not event:
        print("No PushEvent in recent public activity.")
        return None

    repo = event["repo"]["name"].removeprefix("Aayush-25/")
    ago = time_ago(event["created_at"])
    return f"pushed to {repo} · {ago}"


def main() -> None:
    content = README.read_text(encoding="utf-8")
    replacement = fetch_last_push()
    if replacement is None:
        print("Skipping update — API unavailable or no push events found.")
        return

    # Replaces everything after 'last_push  →  ' on that line (idempotent across runs)
    new_content = re.sub(
        r"(  last_push  →  ).*",
        lambda m: m.group(1) + replacement,
        content,
    )

    if new_content == content:
        print("No change.")
        return

    README.write_text(new_content, encoding="utf-8")
    print(f"Updated: {replacement}")


if __name__ == "__main__":
    main()
