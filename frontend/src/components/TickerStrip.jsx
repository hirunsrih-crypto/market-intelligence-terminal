import { useTheme } from "../context/ThemeContext";
import { TrendingUp, TrendingDown } from "lucide-react";

export default function TickerStrip({ indices = [], fx = [], commodities = [] }) {
  const { theme } = useTheme();

  const items = [
    ...indices.slice(0, 8).map((i) => ({ label: i.ticker, value: i.value, change: i.change })),
    ...fx.slice(0, 5).map((f) => ({ label: f.pair, value: f.rate, change: f.change })),
    ...commodities.slice(0, 4).map((c) => ({ label: c.ticker, value: c.value, change: c.change })),
  ].filter((i) => i.value !== null);

  if (items.length === 0) return null;

  const doubled = [...items, ...items];

  return (
    <div
      style={{
        background: theme.bgSecondary,
        borderBottom: `1px solid ${theme.border}`,
        overflow: "hidden",
        position: "relative",
        height: 34,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 32,
          animation: "ticker-scroll 60s linear infinite",
          whiteSpace: "nowrap",
          paddingTop: 6,
          paddingBottom: 6,
        }}
      >
        {doubled.map((item, idx) => {
          const up = item.change >= 0;
          return (
            <span
              key={idx}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                fontSize: 12,
                color: theme.textSecondary,
                flexShrink: 0,
              }}
            >
              <span style={{ color: theme.textPrimary, fontWeight: 600 }}>{item.label}</span>
              <span>{item.value?.toLocaleString("en-US", { maximumFractionDigits: 2 })}</span>
              <span
                style={{
                  color: up ? theme.positive : theme.negative,
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 2,
                }}
              >
                {up ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
                {item.change != null ? `${up ? "+" : ""}${item.change.toFixed(2)}%` : "—"}
              </span>
            </span>
          );
        })}
      </div>

      <style>{`
        @keyframes ticker-scroll {
          from { transform: translateX(0); }
          to   { transform: translateX(-50%); }
        }
      `}</style>
    </div>
  );
}
