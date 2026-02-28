"""
Memory service — lightweight in-memory session store.
Stores user name, discussed topics, and emotional tone per session.
"""

from __future__ import annotations
import re
from typing import Dict, List, Optional
from uuid import uuid4


# In-memory store keyed by session_id
_sessions: Dict[str, dict] = {}

PEOPLE_KEYWORDS = {
    "dad": "father",
    "father": "father",
    "mom": "mother",
    "mother": "mother",
    "friend": "friend",
    "partner": "partner",
    "wife": "partner",
    "husband": "partner",
    "boss": "boss",
    "manager": "boss",
    "brother": "brother",
    "sister": "sister",
}

EMOTION_KEYWORDS = {
    "stress": "stress",
    "stressed": "stress",
    "sad": "sadness",
    "down": "sadness",
    "miss": "sadness",
    "anxious": "anxiety",
    "anxiety": "anxiety",
    "worried": "anxiety",
    "confused": "confusion",
    "lost": "confusion",
}

SITUATION_KEYWORDS = {
    "work": "work pressure",
    "job": "work pressure",
    "exam": "studies",
    "college": "studies",
    "relationship": "relationship strain",
    "breakup": "relationship strain",
    "family": "family tension",
    "hospital": "health concern",
    "money": "financial pressure",
}


def _merge_unique(existing: List[str], new_items: List[str], limit: int = 12) -> List[str]:
    merged = existing[:]
    for item in new_items:
        if item and item not in merged:
            merged.append(item)
    return merged[-limit:]


def _extract_entities(text: str) -> dict:
    lowered = text.lower()

    people: List[str] = []
    for key, value in PEOPLE_KEYWORDS.items():
        if re.search(rf"\b{re.escape(key)}\b", lowered):
            people.append(value)

    emotions: List[str] = []
    for key, value in EMOTION_KEYWORDS.items():
        if re.search(rf"\b{re.escape(key)}\b", lowered):
            emotions.append(value)

    situations: List[str] = []
    for key, value in SITUATION_KEYWORDS.items():
        if re.search(rf"\b{re.escape(key)}\b", lowered):
            situations.append(value)

    return {
        "people": sorted(set(people)),
        "emotions": sorted(set(emotions)),
        "situations": sorted(set(situations)),
    }


def create_session() -> str:
    """Create a new session and return its ID."""
    sid = str(uuid4())
    _sessions[sid] = {
        "user_name": None,
        "topics": [],
        "emotional_tone": [],
        "history": [],  # list of {"role": "user"|"assistant", "content": str}
        "entities": {
            "people": ["father"],
            "emotions": ["stress"],
            "situations": ["family tension"],
        },
        "key_moments": ["User has mentioned missing their father."],
    }
    return sid


def get_session(session_id: str) -> Optional[dict]:
    return _sessions.get(session_id)


def update_session(session_id: str, *, user_name: Optional[str] = None, topic: Optional[str] = None, tone: Optional[str] = None):
    s = _sessions.get(session_id)
    if not s:
        return
    if user_name:
        s["user_name"] = user_name
    if topic and topic not in s["topics"][-5:]:
        s["topics"].append(topic)
        s["topics"] = s["topics"][-10:]  # keep last 10
    if tone:
        s["emotional_tone"].append(tone)
        s["emotional_tone"] = s["emotional_tone"][-10:]


def add_message(session_id: str, role: str, content: str):
    s = _sessions.get(session_id)
    if not s:
        return
    s["history"].append({"role": role, "content": content})
    # Keep last 20 messages for short-term memory
    s["history"] = s["history"][-20:]

    if role == "user" and content.strip():
        entities = _extract_entities(content)
        current = s.get("entities", {"people": [], "emotions": [], "situations": []})

        current["people"] = _merge_unique(current.get("people", []), entities["people"])
        current["emotions"] = _merge_unique(current.get("emotions", []), entities["emotions"])
        current["situations"] = _merge_unique(current.get("situations", []), entities["situations"])
        s["entities"] = current

        if entities["people"] or entities["emotions"] or entities["situations"]:
            s["key_moments"] = _merge_unique(
                s.get("key_moments", []),
                [f"User said: {content[:120]}"],
                limit=8,
            )


def get_history(session_id: str) -> List[dict]:
    s = _sessions.get(session_id)
    if not s:
        return []
    return s["history"]


def get_memory_context(session_id: str) -> str:
    """Build a short memory summary to inject into the prompt."""
    s = _sessions.get(session_id)
    if not s:
        return ""
    parts = []
    if s["user_name"]:
        parts.append(f"User's name: {s['user_name']}")
    if s["topics"]:
        parts.append(f"Topics discussed: {', '.join(s['topics'][-5:])}")
    if s["emotional_tone"]:
        parts.append(f"Recent emotional tones: {', '.join(s['emotional_tone'][-3:])}")
    entities = s.get("entities", {})
    if entities.get("people"):
        parts.append(f"People mentioned: {', '.join(entities['people'][-5:])}")
    if entities.get("emotions"):
        parts.append(f"Emotions mentioned: {', '.join(entities['emotions'][-5:])}")
    if entities.get("situations"):
        parts.append(f"Situations mentioned: {', '.join(entities['situations'][-5:])}")
    if s.get("key_moments"):
        parts.append(f"Key moments: {' | '.join(s['key_moments'][-3:])}")
    return "\n".join(parts)
