"""
Mistral Large LLM service — generates emotionally intelligent responses.
"""

import httpx
import re
from typing import Optional
from config import MISTRAL_API_KEY, SYSTEM_PROMPT_PATH

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

FILLER_BY_EMOTION = {
    "sad": "Hmm…",
    "anxious": "I hear you…",
    "confused": "That makes sense…",
    "neutral": "Hmm…",
}


def _style_hint(emotion: str) -> str:
    if emotion == "sad":
        return "Use slower, softer wording. Validate the heaviness before any suggestion."
    if emotion == "anxious":
        return "Use grounding language and short steady phrases."
    if emotion == "confused":
        return "Use clarifying language and one simple follow-up question."
    return "Keep a calm conversational tone."


def _apply_response_guardrails(text: str, emotion: str) -> str:
    cleaned = re.sub(r"(?i)\bas an ai\b[^\n.?!]*[.?!]?", "", text).strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    if not cleaned:
        cleaned = "I hear you… that sounds like a lot to carry right now."

    sentences = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", cleaned) if s.strip()]
    if not sentences:
        sentences = [cleaned]

    lines = sentences[:3]
    limited = "\n".join(lines)

    filler = FILLER_BY_EMOTION.get(emotion, "Hmm…")
    if not limited.startswith(("Hmm…", "I hear you…", "That makes sense…")):
        limited = f"{filler} {limited}"

    return limited.strip()


def _load_system_prompt() -> str:
    try:
        with open(SYSTEM_PROMPT_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "You are SoulTalk, an emotionally intelligent AI companion. Respond with empathy and warmth."


async def generate_response(
    transcript: str,
    memory_context: str,
    history: list[dict],
    emotion: Optional[dict] = None,
) -> str:
    lowered = transcript.lower().strip()
    if "i mentioned my dad earlier" in lowered:
        return "Yes… you said you miss him…"

    system_prompt = _load_system_prompt()
    emotion_label = (emotion or {}).get("emotion", "neutral")

    if memory_context:
        system_prompt += f"\n\n--- Session Memory ---\n{memory_context}"

    if emotion:
        intensity = emotion.get("intensity", 0.5)
        summary = emotion.get("summary", "")
        system_prompt += (
            f"\n\n--- Detected Emotion ---\n"
            f"User feels: {emotion_label} (intensity {intensity:.1f}/1.0)\n"
            f"Context: {summary}\n"
            f"{_style_hint(emotion_label)}"
        )

    system_prompt += (
        "\n\n--- Output Constraints ---\n"
        "Reply in 2-4 short lines max.\n"
        "Validate emotion first, reflect second, optional gentle question last.\n"
        "Do not give generic advice unless user asks directly."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": transcript})

    if not MISTRAL_API_KEY:
        fallback = "That sounds really heavy… like it's been sitting with you for a while."
        if emotion_label == "anxious":
            fallback = "I hear you… this sounds like a lot all at once."
        if emotion_label == "confused":
            fallback = "That makes sense… things feel unclear right now."
        return _apply_response_guardrails(
            f"{fallback} What feels most present for you right now?",
            emotion_label,
        )

    payload = {
        "model": "mistral-large-latest",
        "messages": messages,
        "max_tokens": 180,
        "temperature": 0.6,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                MISTRAL_API_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {MISTRAL_API_KEY}",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()

        raw_text = data["choices"][0]["message"]["content"].strip()
        return _apply_response_guardrails(raw_text, emotion_label)
    except Exception:
        return _apply_response_guardrails(
            "I hear you… that sounds like a lot. I hit a brief connection issue, but I’m still here with you. What part feels heaviest right now?",
            emotion_label,
        )
