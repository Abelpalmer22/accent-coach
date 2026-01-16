from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    _ = await file.read()
    return {
        "transcript": "hello world",
        "words": [
            {"text": "hello", "start_ms": 0, "end_ms": 500},
            {"text": "world", "start_ms": 500, "end_ms": 1000},
        ],
        "feedback": [],
    }

