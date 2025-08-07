import os
import json
from pathlib import Path
from datetime import datetime
import requests

# === CONFIG ===
SCAN_FOLDER = Path(__file__).parent.resolve()
DATA_FOLDER = SCAN_FOLDER / "data"
STATE_FILE = DATA_FOLDER / "last_state.json"
API_URL = "http://192.168.100.6:5000/upload"  # CHANGE THIS to your phone IP

DATA_FOLDER.mkdir(exist_ok=True)

# === Get full snapshot recursively ===
def get_snapshot(folder: Path, base_path=SCAN_FOLDER):
    snapshot = {}
    for item in folder.rglob("*"):
        if DATA_FOLDER in item.parents:
            continue  # Ignore internal folder
        if item.is_file():
            rel_path = str(item.relative_to(base_path)).replace("\\", "/")
            snapshot[rel_path] = {
                "type": "file",
                "size": item.stat().st_size,
                "created": item.stat().st_ctime,
                "modified": item.stat().st_mtime,
            }
    return snapshot

# === Load previous snapshot ===
if STATE_FILE.exists():
    with open(STATE_FILE, "r") as f:
        old_snapshot = json.load(f)
else:
    old_snapshot = {}

# === Get current snapshot ===
current_snapshot = get_snapshot(SCAN_FOLDER)

# === Detect new or modified files ===
to_send = []

for path, info in current_snapshot.items():
    if path not in old_snapshot:
        to_send.append(path)
    elif "modified" not in old_snapshot[path] or info["modified"] != old_snapshot[path]["modified"]:
        to_send.append(path)

# === Send function ===
def send_file(rel_path: str):
    filepath = SCAN_FOLDER / rel_path
    try:
        with open(filepath, "rb") as f:
            files = {"file": (rel_path, f)}  # rel_path includes folders
            response = requests.post(API_URL, files=files)
            if response.ok:
                print(f"📤 Sent: {rel_path}")
            else:
                print(f"❌ Failed to send {rel_path}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending {rel_path}: {e}")

# === Send new or updated files ===
if to_send:
    print(f"📦 {len(to_send)} file(s) to send.")
    for path in to_send:
        send_file(path)
else:
    print("✅ No new or modified files.")

# === Save new snapshot ===
with open(STATE_FILE, "w") as f:
    json.dump(current_snapshot, f, indent=2)

print(f"✅ Done at {datetime.now().strftime('%H:%M:%S')}")
