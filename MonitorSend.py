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

# === Ensure data folder exists ===
DATA_FOLDER.mkdir(exist_ok=True)

# === Helper: Get directory snapshot ===
def get_snapshot(folder: Path):
    snapshot = {}
    for item in folder.iterdir():
        if item == DATA_FOLDER:
            continue  # Ignore internal folder
        if item.is_file():
            info = {
                "type": "file",
                "size": item.stat().st_size,
                "created": item.stat().st_ctime,
                "modified": item.stat().st_mtime,
            }
            snapshot[item.name] = info
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

for name, info in current_snapshot.items():
    if name not in old_snapshot:
        to_send.append(name)
    elif "modified" not in old_snapshot[name] or info["modified"] != old_snapshot[name]["modified"]:
        to_send.append(name)

# === Send function ===
def send_file(filepath: Path):
    try:
        with open(filepath, "rb") as f:
            files = {"file": (filepath.name, f)}
            response = requests.post(API_URL, files=files)
            if response.ok:
                print(f"📤 Sent: {filepath.name}")
            else:
                print(f"❌ Failed to send {filepath.name}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending {filepath.name}: {e}")

# === Send new or updated files ===
if to_send:
    print(f"📦 {len(to_send)} file(s) to send.")
    for filename in to_send:
        file_path = SCAN_FOLDER / filename
        send_file(file_path)
else:
    print("✅ No new or modified files.")

# === Save new snapshot ===
with open(STATE_FILE, "w") as f:
    json.dump(current_snapshot, f, indent=2)

print(f"✅ Done at {datetime.now().strftime('%H:%M:%S')}")
