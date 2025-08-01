from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/diarize_and_translate")
async def diarize_and_translate(
    audio: UploadFile = File(...),
    max_speakers: int = Form(...),
    target_lang: str = Form(...)
):
    session_id = str(uuid.uuid4())
    temp_dir = f"./temp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)
    audio_path = os.path.join(temp_dir, audio.filename)

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    # Временно возвращаем фиктивный результат
    fake_response = {
        "participants": [
            {
                "speaker": "SPEAKER_00",
                "text": "Привет, как дела?",
                "translation": "Hello, how are you?"
            },
            {
                "speaker": "SPEAKER_01",
                "text": "Отлично, спасибо.",
                "translation": "Great, thank you."
            }
        ]
    }

    try:
        os.remove(audio_path)
        os.rmdir(temp_dir)
    except Exception:
        pass

    return JSONResponse(content=fake_response)

    if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=False)
