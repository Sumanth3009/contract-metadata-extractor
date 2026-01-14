from fastapi import FastAPI, UploadFile, File
import shutil, os
from app.pipeline import run

app = FastAPI()
os.makedirs("uploads", exist_ok=True)

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    path = "uploads/" + file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return run(path)
