import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet

# === SETTINGS ===
STATE_FILE = Path("data/last_state.json")
ENCRYPTED_FILE = Path("data/encrypted_result.bin")
KEY_FILE = Path("data/fernet.key")
SCAN_FOLDER = Path(__file__).parent.resolve()
API_URL = "http://127.0.0.1:8000/upload"  # <-- adjust if needed

# === Ensure data folder exists ===
Path("data").mkdir(exist_ok=True)

# === Load or generate key ===
if not KEY_FILE.exists():
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
else:
    key = KEY_FILE.read_bytes()
fernet = Fernet(key)

# === Snapshot function ===
def get_snapshot(folder: Path):
    snapshot = {}
    for item in folder.iterdir():
        if item.name == "data" or item.name == __file__:
            continue  # skip data folder or script itself
        info = {
            "type": "file" if item.is_file() else "folder",
            "size": item.stat().st_size,
            "created": item.stat().st_ctime,
        }
        if item.is_file():
            try:
                info["content"] = item.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                info["content"] = f"<Unreadable: {e}>"
        snapshot[item.name] = info
    return snapshot

# === Load old snapshot ===
old_snapshot = {}
if STATE_FILE.exists():
    with open(STATE_FILE, "r") as f:
        old_snapshot = json.load(f)

# === Get current snapshot ===
current_snapshot = get_snapshot(SCAN_FOLDER)

# === Compare ===
new_items = {
    name: info for name, info in current_snapshot.items()
    if name not in old_snapshot
}

# === Encrypt & Save ===
if new_items:
    json_data = json.dumps(new_items, indent=2).encode("utf-8")
    encrypted = fernet.encrypt(json_data)
    ENCRYPTED_FILE.write_bytes(encrypted)
    print(f"🔐 Encrypted {len(new_items)} new item(s).")

    # === Send to API ===
    try:
        print("📡 Sending to server...")
        with open(ENCRYPTED_FILE, "rb") as f:
            response = requests.post(
                API_URL,
                files={"file": ("encrypted_result.bin", f, "application/octet-stream")}
            )
        print("📬 Server response:", response.json())
    except Exception as e:
        print("❌ Failed to send to server:", e)
else:
    print("✅ No new files or folders since last run.")

# === Save current snapshot for next time ===
with open(STATE_FILE, "w") as f:
    json.dump(current_snapshot, f, indent=2)

print("✅ Directory check complete.")
