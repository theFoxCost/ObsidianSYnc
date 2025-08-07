from flask import Flask, request
from pathlib import Path
import os

app = Flask(__name__)
save_path = Path("received_files")
save_path.mkdir(exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files['file']
    rel_path = uploaded_file.filename.replace("\\", "/")
    full_path = save_path / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    uploaded_file.save(full_path)
    return f"✅ File saved: {rel_path}", 200

app.run(host="0.0.0.0", port=5000)
