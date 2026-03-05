import { useTheme } from "../context/ThemeContext";
import { TrendingUp, TrendingDown } from "lucide-react";

const ICONS = {
  Gold: "Au", Brent: "OIL", Wti: "WTI", Silver: "Ag", Copper: "Cu", Natgas: "GAS",
};

export default function CommoditiesPanel({ commodities = [] }) {
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
          Commodities
        </span>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 1,
          background: theme.borderSubtle,
        }}
      >
        {commodities.length === 0 &&
          Array(6).fill(0).map((_, i) => (
            <div key={i} style={{ background: theme.bgCard, padding: "14px 16px" }}>
              <div style={{ color: theme.textMuted, fontSize: 12 }}>Loading...</div>
            </div>
          ))
        }
        {commodities.map((c) => {
          const up = c.change >= 0;
          const label = c.name.charAt(0).toUpperCase() + c.name.slice(1).toLowerCase();
          return (
            <div
              key={c.ticker}
              style={{
                background: theme.bgCard,
                padding: "14px 16px",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <div>
                  <div style={{ fontSize: 11, color: theme.textMuted, fontWeight: 600, letterSpacing: "0.05em" }}>
                    {ICONS[label] || c.ticker}
                  </div>
                  <div style={{ fontSize: 13, color: theme.textPrimary, fontWeight: 600, marginTop: 2 }}>
                    {label}
                  </div>
                </div>
                <span
                  style={{
                    fontSize: 10,
                    color: theme.textMuted,
                    background: theme.tagBg,
                    borderRadius: 4,
                    padding: "2px 5px",
                  }}
                >
                  {c.unit}
                </span>
              </div>
              <div style={{ marginTop: 8 }}>
                <div style={{ fontSize: 15, fontWeight: 600, color: theme.textPrimary }}>
                  {c.value != null ? `$${c.value.toLocaleString("en-US", { maximumFractionDigits: 2 })}` : "—"}
                </div>
                <div
                  style={{
                    fontSize: 12,
                    color: up ? theme.positive : theme.negative,
                    display: "flex",
                    alignItems: "center",
                    gap: 3,
                    marginTop: 2,
                  }}
                >
                  {c.change != null ? (
                    <>
                      {up ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                      {up ? "+" : ""}{c.change.toFixed(2)}%
                    </>
                  ) : "—"}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
