"""
SoulTalk AI — Backend API
"""

import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from services.voxtral_service import transcribe_audio
from services.mistral_service import generate_response
from services.elevenlabs_service import text_to_speech
from services.emotion_service import detect_emotion
from services.memory_service import (
    create_session,
    get_session,
    add_message,
    get_history,
    get_memory_context,
    update_session,
)

app = FastAPI(title="SoulTalk AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "app": "SoulTalk AI"}


@app.post("/session")
async def new_session():
    sid = create_session()
    return {"session_id": sid}


@app.post("/chat")
async def full_chat(audio: UploadFile = File(...), session_id: str = ""):
    """Full pipeline: audio → transcript → emotion → AI response → TTS."""
    try:
        audio_bytes = await audio.read()
        mime = audio.content_type or "audio/wav"
        transcript = await transcribe_audio(audio_bytes, mime)

        if not session_id or not get_session(session_id):
            session_id = create_session()

        add_message(session_id, "user", transcript)

        memory = get_memory_context(session_id)
        history = get_history(session_id)
        emotion_data = await detect_emotion(transcript)

        response_text = await generate_response(
            transcript, memory, history, emotion=emotion_data
        )
        add_message(session_id, "assistant", response_text)
        update_session(
            session_id,
            topic=transcript[:50],
            tone=emotion_data.get("emotion", "neutral"),
        )

        tts_audio = await text_to_speech(response_text)
        audio_b64 = base64.b64encode(tts_audio).decode("utf-8") if tts_audio else ""

        return {
            "transcript": transcript,
            "response": response_text,
            "emotion": emotion_data,
            "audio_base64": audio_b64,
            "session_id": session_id,
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "chat_pipeline_failed", "detail": str(e)},
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
