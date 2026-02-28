import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAudioRecorder } from "../hooks/useAudioRecorder";
import { createSession, fullChat } from "../api";
import WaveAnimation from "../components/WaveAnimation";
import MessageBubble from "../components/MessageBubble";
import EmotionBadge from "../components/EmotionBadge";
import ThinkingIndicator from "../components/ThinkingIndicator";

type Emotion = {
  emotion: string;
  intensity: number;
  summary: string;
};

type Message = {
  role: "user" | "assistant";
  text: string;
  emotion?: Emotion;
};

export default function Chat() {
  const navigate = useNavigate();
  const { isRecording, startRecording, stopRecording } = useAudioRecorder();
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [status, setStatus] = useState<"idle" | "recording" | "thinking" | "speaking">("idle");
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  const [latestEmotion, setLatestEmotion] = useState<Emotion | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Create session on mount
  useEffect(() => {
    createSession().then(setSessionId).catch(() => setSessionId("demo"));
  }, []);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, status]);

  const handleMicClick = async () => {
    if (status === "speaking" && currentAudio) {
      currentAudio.pause();
      setCurrentAudio(null);
      setStatus("idle");
      return;
    }

    if (isRecording) {
      // Stop recording → process
      const audioBlob = await stopRecording();
      setStatus("thinking");

      try {
        const result = await fullChat(audioBlob, sessionId);

        if (result.session_id) setSessionId(result.session_id);

        // Extract emotion
        const emotion = result.emotion || null;
        if (emotion) setLatestEmotion(emotion);

        // Add user message
        setMessages((prev) => [...prev, { role: "user", text: result.transcript, emotion: emotion || undefined }]);

        // Slight pause to feel more human
        await new Promise((resolve) => setTimeout(resolve, 450));

        // Add AI response
        setMessages((prev) => [...prev, { role: "assistant", text: result.response }]);

        // Play TTS audio if available
        if (result.audio_base64) {
          setStatus("speaking");
          const audio = new Audio(`data:audio/mpeg;base64,${result.audio_base64}`);
          setCurrentAudio(audio);
          audio.onended = () => {
            setStatus("idle");
            setCurrentAudio(null);
          };
          audio.play().catch(() => setStatus("idle"));
        } else {
          setStatus("idle");
        }
      } catch (err) {
        console.error("Pipeline error:", err);
        const errorMessage =
          err instanceof Error && err.message
            ? err.message
            : "I had trouble hearing you. Could you try again?";
        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: `I hit an issue: ${errorMessage}` },
        ]);
        setStatus("idle");
      }
    } else {
      // Start recording
      await startRecording();
      setStatus("recording");
    }
  };

  const statusText = {
    idle: "Tap to speak",
    recording: "Listening...",
    thinking: "Reflecting...",
    speaking: "Speaking...",
  };

  const micColors = {
    idle: "from-violet-600 to-fuchsia-600",
    recording: "from-red-500 to-rose-500",
    thinking: "from-amber-500 to-orange-500",
    speaking: "from-emerald-500 to-teal-500",
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-950 relative overflow-hidden">
      {/* Ambient background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-violet-600/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-1/4 w-[400px] h-[300px] bg-fuchsia-600/5 rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-4 border-b border-gray-800/50 glass">
        <button
          onClick={() => navigate("/")}
          className="text-gray-400 hover:text-white transition-colors text-sm flex items-center gap-1.5 cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Back
        </button>
        <h1 className="text-lg font-semibold text-shimmer">
          SoulTalk
        </h1>
        <div className="flex items-center gap-2">
          {latestEmotion && (
            <EmotionBadge
              emotion={latestEmotion.emotion}
              intensity={latestEmotion.intensity}
              summary={latestEmotion.summary}
            />
          )}
        </div>
      </header>

      {/* Messages area */}
      <div className="relative z-10 flex-1 overflow-y-auto px-6 py-6 space-y-5">
        {messages.length === 0 && status === "idle" && (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500 mt-16 animate-fade-in-up">
            {/* Animated orb */}
            <div className="relative mb-6">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-violet-500/20 to-fuchsia-500/20 flex items-center justify-center animate-breathe">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-violet-500/30 to-fuchsia-500/30 flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-7 h-7 text-violet-400 animate-float" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
              </div>
            </div>
            <p className="text-xl font-light text-gray-300">I'm here. Whenever you're ready.</p>
            <p className="text-sm text-gray-600 mt-2">Tap the mic below to start talking</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className="space-y-1.5">
            <MessageBubble role={msg.role} text={msg.text} />
            {msg.emotion && msg.role === "user" && (
              <div className="flex justify-end pr-11">
                <EmotionBadge
                  emotion={msg.emotion.emotion}
                  intensity={msg.emotion.intensity}
                  summary={msg.emotion.summary}
                />
              </div>
            )}
          </div>
        ))}

        {/* Thinking indicator */}
        {status === "thinking" && <ThinkingIndicator />}

        <div ref={messagesEndRef} />
      </div>

      {/* Wave animation */}
      {(status === "recording" || status === "speaking") && (
        <div className="relative z-10 flex justify-center py-3 animate-fade-in">
          <WaveAnimation
            active={true}
            color={status === "recording" ? "red" : "green"}
          />
        </div>
      )}

      {/* Bottom controls */}
      <div className="relative z-10 flex flex-col items-center pb-8 pt-4">
        <p className={`text-sm mb-4 transition-all duration-300 ${
          status === "recording" ? "text-red-400 font-medium" :
          status === "thinking" ? "text-amber-400" :
          status === "speaking" ? "text-emerald-400" :
          "text-gray-500"
        }`}>
          {statusText[status]}
        </p>

        {/* Mic button with glow effects */}
        <div className="relative">
          {/* Outer glow ring */}
          {status === "idle" && (
            <div className="absolute inset-0 -m-3 rounded-full bg-gradient-to-br from-violet-500/10 to-fuchsia-500/10 animate-breathe" />
          )}

          <button
            onClick={handleMicClick}
            disabled={status === "thinking"}
            className={`relative w-20 h-20 rounded-full bg-gradient-to-br ${micColors[status]} flex items-center justify-center shadow-lg transition-all duration-300 hover:scale-110 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer`}
          >
            {/* Pulse rings when recording */}
            {status === "recording" && (
              <>
                <span className="absolute inset-0 rounded-full bg-red-500/30 animate-pulse-ring" />
                <span className="absolute inset-0 rounded-full bg-red-500/20 animate-pulse-ring-slow" />
                <span className="absolute inset-0 -m-2 rounded-full bg-red-500/10 animate-pulse-ring" style={{ animationDelay: "0.7s" }} />
              </>
            )}

            {/* Speaking pulse */}
            {status === "speaking" && (
              <>
                <span className="absolute inset-0 rounded-full bg-emerald-500/25 animate-pulse-ring-slow" />
              </>
            )}

            {status === "thinking" ? (
              /* Spinner */
              <svg className="w-8 h-8 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
            ) : status === "speaking" ? (
              /* Stop/Speaker icon */
              <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.536 8.464a5 5 0 010 7.072M18.364 5.636a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              </svg>
            ) : (
              /* Mic icon */
              <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
