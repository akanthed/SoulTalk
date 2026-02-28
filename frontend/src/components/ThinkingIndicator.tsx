export default function ThinkingIndicator() {
  return (
    <div className="flex justify-start animate-fade-in">
      {/* Avatar */}
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center mr-3 mt-1 shadow-lg shadow-violet-500/20 animate-breathe">
        <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      </div>

      <div className="glass rounded-2xl rounded-bl-sm border border-gray-700/20 px-5 py-4">
        <span className="text-[11px] text-violet-400/80 font-semibold tracking-wide uppercase block mb-2">
          SoulTalk
        </span>
        <div className="flex items-center gap-1.5">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 rounded-full bg-violet-400/60 animate-bounce"
              style={{ animationDelay: `${i * 0.2}s`, animationDuration: "1s" }}
            />
          ))}
          <span className="text-xs text-gray-500 ml-2">reflecting...</span>
        </div>
      </div>
    </div>
  );
}
