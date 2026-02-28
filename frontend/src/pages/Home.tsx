import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-violet-600/8 rounded-full blur-3xl animate-breathe pointer-events-none" />

      {/* Content */}
      <div className="relative z-10 text-center max-w-lg animate-fade-in-up">
        {/* Logo */}
        <div className="relative mx-auto mb-10 w-24 h-24">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center shadow-2xl shadow-violet-500/30 animate-breathe">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-11 h-11 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.5}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z"
              />
            </svg>
          </div>
        </div>

        <h1 className="text-6xl font-bold tracking-tight mb-5 text-shimmer">
          Talk. I'm here.
        </h1>

        <p className="text-gray-400 text-lg mb-12 leading-relaxed max-w-sm mx-auto">
          SoulTalk AI listens with empathy and responds with heart.
          <br />
          <span className="text-gray-500">No judgment. Just presence.</span>
        </p>

        <button
          onClick={() => navigate("/chat")}
          className="group relative inline-flex items-center gap-3 px-10 py-5 bg-gradient-to-r from-violet-600 to-fuchsia-600 rounded-full text-white font-semibold text-lg hover:from-violet-500 hover:to-fuchsia-500 transition-all duration-300 shadow-xl shadow-violet-500/25 hover:shadow-violet-500/40 hover:scale-105 active:scale-95 cursor-pointer"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z"
            />
          </svg>
          <span>Start Talking</span>
        </button>
      </div>

      <p className="absolute bottom-6 text-gray-700 text-xs tracking-wider uppercase">
        SoulTalk AI — your empathetic companion
      </p>
    </div>
  );
}
