from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import os
import tempfile


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- ADD THIS BLOCK HERE ----
# Load model once at startup
model = WhisperModel("small", device="cpu", compute_type="int8")
# ------------------------------

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()

    # Write upload to a temporary file (keeps faster-whisper happy)
    suffix = ""
    if file.filename and "." in file.filename:
        suffix = os.path.splitext(file.filename)[1]  # e.g. ".m4a"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        segments, info = model.transcribe(tmp_path, language="en")
        transcript = "".join(seg.text for seg in segments).strip()
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    return {
        "transcript": transcript,
        "words": [],
        "feedback": [],
    }




