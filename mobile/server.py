from flask import Flask, request
from pathlib import Path

app = Flask(__name__)
save_path = Path("received_files")  # This saves in the script's own directory
save_path.mkdir(exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    full_path = save_path / filename
    uploaded_file.save(full_path)
    return f"✅ File saved: {filename}", 200

app.run(host="0.0.0.0", port=5000)
