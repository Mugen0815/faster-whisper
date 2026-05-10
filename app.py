import os
import uuid
from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel

MODEL_NAME = os.getenv("WHISPER_MODEL", "large-v3")
DEVICE = os.getenv("WHISPER_DEVICE", "cuda")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "float16")

app = FastAPI(title="Whisper API")

model_instance = WhisperModel(
    MODEL_NAME,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

def run_transcription(input_path: str):
    segments, info = model_instance.transcribe(input_path)
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return {
        "text": text,
        "language": info.language,
        "duration": info.duration
    }

@app.get("/health")
def health():
    return {"ok": True, "model": MODEL_NAME, "device": DEVICE}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "audio")[1] or ".bin"
    path = f"/tmp/audio/{uuid.uuid4()}{suffix}"

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        result = run_transcription(path)
    finally:
        try:
            os.remove(path)
        except:
            pass

    return result

@app.post("/audio/transcriptions")
async def audio_transcriptions(
    file: UploadFile = File(...),
    model: str = "whisper-1"
):
    suffix = os.path.splitext(file.filename or "audio")[1] or ".bin"
    path = f"/tmp/audio/{uuid.uuid4()}{suffix}"

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        result = run_transcription(path)
    finally:
        try:
            os.remove(path)
        except:
            pass

    return result