# SoulTalk AI 🧠💬

**Voice-first emotional AI companion** — Talk, and it listens with empathy.

Built for hackathon in 2 days. Prioritizes demo impact over production readiness.

---

## How It Works

1. **You speak** → Microphone captures audio
2. **Voxtral** → Speech-to-text transcription (Mistral multimodal)
3. **Mistral Large** → Generates emotionally intelligent response
4. **ElevenLabs** → Text-to-speech with natural voice
5. **You hear** → AI responds with warmth and empathy

---

## Tech Stack

| Layer     | Tech                        |
| --------- | --------------------------- |
| Frontend  | React (Vite) + TailwindCSS  |
| Backend   | Python FastAPI              |
| STT       | Voxtral (Mistral)           |
| LLM       | Mistral Large               |
| TTS       | ElevenLabs                  |
| Memory    | In-memory JSON (per session)|

---

## Quick Start

### 1. Backend

```bash
cd backend
pip install -r requirements.txt

# Create .env file with your API keys
cp .env.example .env
# Edit .env and add your keys:
#   MISTRAL_API_KEY=your_key
#   ELEVENLABS_API_KEY=your_key
#   ELEVENLABS_VOICE_ID=your_voice_id

python main.py
```

Backend runs on **http://localhost:8000**

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on **http://localhost:5173**

The frontend proxies API requests to the backend automatically.

---

## API Keys Required

| Service     | Get Key At                                    |
| ----------- | --------------------------------------------- |
| Mistral     | https://console.mistral.ai/                   |
| ElevenLabs  | https://elevenlabs.io/                         |

> **Demo mode**: If no API keys are set, the backend returns mock responses so you can test the UI flow.

---

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app with all routes
│   ├── config.py             # Environment config
│   ├── requirements.txt
│   ├── .env.example
│   └── services/
│       ├── voxtral_service.py    # Speech-to-text
│       ├── mistral_service.py    # LLM response generation
│       ├── elevenlabs_service.py # Text-to-speech
│       └── memory_service.py     # Session memory
├── frontend/
│   ├── src/
│   │   ├── main.tsx          # Entry point
│   │   ├── App.tsx           # Router
│   │   ├── api.ts            # Backend API client
│   │   ├── pages/
│   │   │   ├── Home.tsx      # Landing page
│   │   │   └── Chat.tsx      # Chat interface
│   │   ├── components/
│   │   │   ├── WaveAnimation.tsx
│   │   │   └── MessageBubble.tsx
│   │   └── hooks/
│   │       └── useAudioRecorder.ts
│   └── index.html
└── prompts/
    └── system_prompt.txt     # AI personality prompt
```

---

## Features

- 🎤 Voice input with real-time recording
- 🧠 Emotionally intelligent AI responses
- 🔊 Natural text-to-speech output
- 💾 Session memory (topics, emotional tone)
- 🌊 Audio wave animations
- 🎨 Clean, minimal dark UI
- 🤖 Human-like response delays and fillers

---

## License

Hackathon project — use freely.
