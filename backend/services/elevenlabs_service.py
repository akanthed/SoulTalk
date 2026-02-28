"""
ElevenLabs text-to-speech service.
Converts AI response text to natural-sounding speech audio.
"""

import httpx
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID


def _prepare_tts_text(text: str) -> str:
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""

    lines = [line.strip() for line in cleaned.split("\n") if line.strip()]
    compact = " ... ".join(lines[:4])
    compact = compact.replace(". ", "... ")
    return compact


async def text_to_speech(text: str) -> bytes:
    """
    Convert text to speech using ElevenLabs API.
    Returns raw MP3 audio bytes.
    """
    if not ELEVENLABS_API_KEY:
        # Return empty bytes as mock — frontend will handle gracefully
        return b""

    tts_text = _prepare_tts_text(text)
    if not tts_text:
        return b""

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    payload = {
        "text": tts_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.72,
            "similarity_boost": 0.8,
            "style": 0.28,
            "use_speaker_boost": True,
        },
    }

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.content
    except Exception:
        return b""
