from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from datetime import datetime

app = FastAPI()
UPLOAD_FOLDER = Path("server_data")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    path = UPLOAD_FOLDER / filename
    content = await file.read()
    path.write_bytes(content)
    return {"status": "success", "saved_as": str(path)}
