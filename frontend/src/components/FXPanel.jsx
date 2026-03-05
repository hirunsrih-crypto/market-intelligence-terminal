import { useTheme } from "../context/ThemeContext";
import { TrendingUp, TrendingDown } from "lucide-react";

export default function FXPanel({ fx = [] }) {
  const { theme } = useTheme();

  return (
    <div
      style={{
        background: theme.bgCard,
        border: `1px solid ${theme.border}`,
        borderRadius: 10,
        overflow: "hidden",
      }}
    >
      <div style={{ padding: "14px 16px", borderBottom: `1px solid ${theme.border}` }}>
        <span style={{ fontSize: 13, fontWeight: 600, color: theme.textPrimary, letterSpacing: "0.03em" }}>
          FX Rates
        </span>
      </div>

      <div style={{ padding: "8px 0" }}>
        {fx.length === 0 && (
          <div style={{ padding: "24px 16px", color: theme.textMuted, textAlign: "center", fontSize: 13 }}>
            Loading...
          </div>
        )}
        {fx.map((item) => {
          const up = item.change >= 0;
          return (
            <div
              key={item.pair}
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "9px 16px",
                borderBottom: `1px solid ${theme.borderSubtle}`,
              }}
            >
              <span style={{ color: theme.textPrimary, fontWeight: 600, fontSize: 13 }}>{item.pair}</span>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <span style={{ color: theme.textPrimary, fontSize: 13 }}>
                  {item.rate != null ? item.rate.toFixed(4) : "—"}
                </span>
                <span
                  style={{
                    color: up ? theme.positive : theme.negative,
                    fontSize: 12,
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 3,
                    minWidth: 70,
                    justifyContent: "flex-end",
                  }}
                >
                  {item.change != null ? (
                    <>
                      {up ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                      {up ? "+" : ""}{item.change.toFixed(3)}%
                    </>
                  ) : "—"}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
