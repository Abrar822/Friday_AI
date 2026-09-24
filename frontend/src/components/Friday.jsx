import { useId } from "react";

export default function FridayLogo() {
  const instanceId = useId().replace(/:/g, "");

  const ringGradId = `pocketAIRingGrad-${instanceId}`;
  const ringGlowId = `pocketAIRingGlow-${instanceId}`;

  const size = 45;
  const center = size / 2;
  const ringR = 19;

  return (
    <div className="absolute top-[50%] left-[50%] -translate-x-1/2 -translate-y-1/2 flex items-center justify-center">
      <div className="absolute opacity-10 text-(--text-primary) text-[160px] z-2 tracking-widest">FRIDAY</div>
      <svg
      className="animate-[fadeIn_5s_ease-in-out_infinite_alternate] absolute z-1"
      width="300"
      height="300"
      viewBox="0 0 45 45"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        display: "block",
        overflow: "visible",
      }}
      aria-label="Friday"
      role="img"
    >
      <defs>
        {/* Same gradient as the original orb */}
        <linearGradient
          id={ringGradId}
          x1="0%"
          y1="0%"
          x2="100%"
          y2="0%"
        >
          <stop
            offset="0%"
            stopColor="#e94ff5"
          />

          <stop
            offset="30%"
            stopColor="#b06bff"
          />

          <stop
            offset="65%"
            stopColor="#5b8bff"
          />

          <stop
            offset="100%"
            stopColor="#4fd8ff"
          />
        </linearGradient>

        {/* Same glow effect as the original orb */}
        <filter
          id={ringGlowId}
          x="-80%"
          y="-80%"
          width="260%"
          height="260%"
        >
          <feGaussianBlur
            stdDeviation="0.9"
            result="near"
          />

          <feGaussianBlur
            in="SourceGraphic"
            stdDeviation="2.7"
            result="far"
          />

          <feMerge>
            <feMergeNode in="far" />
            <feMergeNode in="near" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Friday glowing ring */}
      <g filter={`url(#${ringGlowId})`}>
        <circle
          cx={center}
          cy={center}
          r={ringR}
          fill="none"
          stroke={`url(#${ringGradId})`}
          strokeWidth="3"
        />
      </g>
    </svg>
    </div>
  );
}