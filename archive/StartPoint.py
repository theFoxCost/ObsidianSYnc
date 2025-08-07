import os
import json
import time
from pathlib import Path
from datetime import datetime
# 1. Set target folder
target_folder = Path(__file__).parent.resolve()
# 2. Start timer
start = time.time()

# 3. Get all contents
all_items = list(target_folder.iterdir())

# 4. Separate files and folders
files = [item.name for item in all_items if item.is_file()]
folders = [item.name for item in all_items if item.is_dir()]

# 5. Print results
print("All items:", [item.name for item in all_items])
print("Folders only:", folders)
print("Files only:", files)

# 6. Wait 1 second
time.sleep(1)

# 7. Create "data" directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# 8. Prepare data
result = {
    "all_items": [item.name for item in all_items],
    "folders": folders,
    "files": files
}

# 9. Save JSON with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
json_path = data_dir / f"folder_content_{timestamp}.json"
with open(json_path, "w") as f:
    json.dump(result, f, indent=2)

# 10. Print finish time
end = time.time()
print(f"✅ Finish in {end - start:.3f} seconds")
