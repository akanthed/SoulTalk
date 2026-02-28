type Props = {
  active: boolean;
  color?: "red" | "green";
};

export default function WaveAnimation({ active, color = "green" }: Props) {
  const barColor = color === "red" ? "bg-red-400" : "bg-emerald-400";

  return (
    <div className="flex items-center gap-1 h-10">
      {Array.from({ length: 7 }).map((_, i) => (
        <div
          key={i}
          className={`w-1 rounded-full transition-all duration-300 ${barColor} ${
            active ? "animate-wave-bar" : "h-1 opacity-40"
          }`}
          style={active ? { animationDelay: `${(i * 0.12).toFixed(2)}s` } : undefined}
        />
      ))}
    </div>
  );
}
