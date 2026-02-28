"""
Emotion detection service.
Uses Mistral to analyse the emotional tone of user messages
and returns a structured emotion label + intensity.
"""

import httpx
from config import MISTRAL_API_KEY

MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"

# Supported emotion labels
EMOTIONS = ["sad", "anxious", "confused", "neutral"]

DETECTION_PROMPT = f"""You are an emotion classifier. Given a user message, respond with ONLY a JSON object (no markdown, no extra text) containing:
- "emotion": one of {EMOTIONS}
- "intensity": a float 0.0–1.0 (0 = barely present, 1 = very intense)
- "summary": a 3-5 word description of the emotional state

Example output:
{{"emotion": "anxious", "intensity": 0.7, "summary": "worried and tense"}}
"""


def _normalize_emotion(label: str) -> str:
    normalized = (label or "").lower().strip()
    if normalized in EMOTIONS:
        return normalized

    map_to_four = {
        "happy": "neutral",
        "angry": "anxious",
        "lonely": "sad",
        "hopeful": "neutral",
        "grateful": "neutral",
        "fearful": "anxious",
        "overwhelmed": "anxious",
        "excited": "neutral",
        "frustrated": "anxious",
        "peaceful": "neutral",
    }
    return map_to_four.get(normalized, "neutral")


async def detect_emotion(text: str) -> dict:
    """
    Analyse a user message and return emotion data.
    Returns dict with keys: emotion, intensity, summary.
    Falls back to a simple keyword-based detector when no API key is set.
    """
    if not MISTRAL_API_KEY:
        return _keyword_fallback(text)

    payload = {
        "model": "mistral-small-latest",
        "messages": [
            {"role": "system", "content": DETECTION_PROMPT},
            {"role": "user", "content": text},
        ],
        "max_tokens": 100,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(MISTRAL_CHAT_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            raw = data["choices"][0]["message"]["content"].strip()

        import json
        result = json.loads(raw)
        # Validate
        result["emotion"] = _normalize_emotion(result.get("emotion", "neutral"))
        result["intensity"] = max(0.0, min(1.0, float(result.get("intensity", 0.5))))
        result.setdefault("summary", result["emotion"])
        return result
    except Exception:
        return _keyword_fallback(text)


def _keyword_fallback(text: str) -> dict:
    """Simple keyword-based emotion detector for offline / demo mode."""
    t = text.lower()

    keyword_map = {
        "sad": ["sad", "depressed", "down", "unhappy", "crying", "tears", "miss", "lonely"],
        "anxious": ["anxious", "worried", "nervous", "stress", "panic", "overwhelm", "afraid", "frustrat", "angry"],
        "confused": ["confused", "lost", "don't know", "unsure", "uncertain"],
    }

    for emotion, keywords in keyword_map.items():
        for kw in keywords:
            if kw in t:
                summary_map = {
                    "sad": "low and heavy",
                    "anxious": "on edge and tense",
                    "confused": "struggling to understand",
                }
                return {
                    "emotion": emotion,
                    "intensity": 0.6,
                    "summary": summary_map.get(emotion, f"feeling {emotion}"),
                }

    return {"emotion": "neutral", "intensity": 0.3, "summary": "neutral tone"}
