const EMOTION_CONFIG: Record<string, { emoji: string; color: string; bg: string }> = {
  happy:       { emoji: "😊", color: "text-yellow-300",  bg: "bg-yellow-500/10 border-yellow-500/20" },
  sad:         { emoji: "😢", color: "text-blue-300",    bg: "bg-blue-500/10 border-blue-500/20" },
  anxious:     { emoji: "😰", color: "text-amber-300",   bg: "bg-amber-500/10 border-amber-500/20" },
  angry:       { emoji: "😤", color: "text-red-300",     bg: "bg-red-500/10 border-red-500/20" },
  confused:    { emoji: "😕", color: "text-orange-300",   bg: "bg-orange-500/10 border-orange-500/20" },
  lonely:      { emoji: "🥺", color: "text-indigo-300",  bg: "bg-indigo-500/10 border-indigo-500/20" },
  hopeful:     { emoji: "🌱", color: "text-emerald-300", bg: "bg-emerald-500/10 border-emerald-500/20" },
  grateful:    { emoji: "🙏", color: "text-pink-300",    bg: "bg-pink-500/10 border-pink-500/20" },
  fearful:     { emoji: "😨", color: "text-purple-300",  bg: "bg-purple-500/10 border-purple-500/20" },
  neutral:     { emoji: "😌", color: "text-gray-300",    bg: "bg-gray-500/10 border-gray-500/20" },
  overwhelmed: { emoji: "😮‍💨", color: "text-rose-300",   bg: "bg-rose-500/10 border-rose-500/20" },
  excited:     { emoji: "🎉", color: "text-fuchsia-300", bg: "bg-fuchsia-500/10 border-fuchsia-500/20" },
  frustrated:  { emoji: "😩", color: "text-orange-300",  bg: "bg-orange-500/10 border-orange-500/20" },
  peaceful:    { emoji: "☁️",  color: "text-cyan-300",   bg: "bg-cyan-500/10 border-cyan-500/20" },
};

type Props = {
  emotion: string;
  intensity?: number;
  summary?: string;
};

export default function EmotionBadge({ emotion, intensity = 0.5, summary }: Props) {
  const config = EMOTION_CONFIG[emotion] || EMOTION_CONFIG.neutral;

  // Intensity bar width (0-100%)
  const barWidth = Math.round(intensity * 100);

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-medium animate-emotion-pop ${config.bg}`}>
      <span className="text-sm">{config.emoji}</span>
      <span className={config.color}>
        {summary || emotion}
      </span>
      {/* Tiny intensity bar */}
      <div className="w-8 h-1 rounded-full bg-white/10 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${config.color.replace("text-", "bg-")}`}
          style={{ width: `${barWidth}%` }}
        />
      </div>
    </div>
  );
}
