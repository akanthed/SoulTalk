"""
Voxtral (Mistral) speech-to-text service.
Uses the Mistral API with the mistral-small-latest model for audio transcription
via the multimodal chat completions endpoint.

Voxtral accepts audio as a data URI inside an audio_url content block.
Supported formats: wav, mp3, flac, ogg, webm (all encoded as base64).
"""

import base64
import httpx
from config import MISTRAL_API_KEY

MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_TRANSCRIBE_URL = "https://api.mistral.ai/v1/audio/transcriptions"

# Map browser MIME types to simplified types Mistral expects
MIME_NORMALISE = {
    "audio/webm": "audio/webm",
    "audio/webm;codecs=opus": "audio/webm",
    "audio/ogg": "audio/ogg",
    "audio/ogg;codecs=opus": "audio/ogg",
    "audio/wav": "audio/wav",
    "audio/x-wav": "audio/wav",
    "audio/mpeg": "audio/mpeg",
    "audio/mp3": "audio/mpeg",
    "audio/flac": "audio/flac",
    "audio/mp4": "audio/mp4",
}


def _normalise_mime(raw: str) -> str:
    return MIME_NORMALISE.get(raw.lower().strip(), "audio/wav")


async def transcribe_audio(audio_bytes: bytes, mime_type: str = "audio/wav") -> str:
    """
    Transcribe audio using Voxtral via Mistral's multimodal chat completions.
    Audio is sent as a base64 data-URI inside an ``audio_url`` content block.
    """
    if not MISTRAL_API_KEY:
        # Mock response for demos without an API key
        return "I've been feeling a bit overwhelmed lately with everything going on."

    mime = _normalise_mime(mime_type)

    # 1) Preferred path: dedicated speech-to-text endpoint
    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Accept": "application/json",
        }

        for model in ["voxtral-mini-latest", "voxtral-small-latest", "mistral-small-latest"]:
            files = {
                "file": ("recording.webm", audio_bytes, mime),
            }
            data = {
                "model": model,
            }

            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    MISTRAL_TRANSCRIBE_URL,
                    headers=headers,
                    data=data,
                    files=files,
                )

            if resp.status_code >= 400:
                continue

            result = resp.json()
            text = (result.get("text") or "").strip()
            if text:
                return text
    except Exception:
        pass

    # 2) Fallback path: multimodal chat with audio data URI
    try:
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        data_uri = f"data:{mime};base64,{audio_b64}"

        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "audio_url",
                            "audio_url": data_uri,
                        },
                        {
                            "type": "text",
                            "text": (
                                "Transcribe the spoken words in this audio exactly as spoken. "
                                "Return ONLY the transcription text — no commentary, no labels, "
                                "no timestamps."
                            ),
                        },
                    ],
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.0,
        }

        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(MISTRAL_CHAT_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        transcript = data["choices"][0]["message"]["content"].strip()
        if transcript.startswith('"') and transcript.endswith('"'):
            transcript = transcript[1:-1]
        if transcript:
            return transcript
    except Exception:
        pass

    return "I couldn't transcribe that clearly. Could you try saying it again?"
