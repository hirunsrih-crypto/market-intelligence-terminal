import { useTheme } from "../context/ThemeContext";

function VIXLevel(vix) {
  if (vix == null) return { label: "N/A", color: null };
  if (vix < 15) return { label: "Low Fear", color: "positive" };
  if (vix < 20) return { label: "Calm", color: "positive" };
  if (vix < 25) return { label: "Elevated", color: "warning" };
  if (vix < 35) return { label: "High Fear", color: "negative" };
  return { label: "Extreme Fear", color: "negative" };
}

function GaugeBar({ value, max, color, theme }) {
  const pct = Math.min((value / max) * 100, 100);
  return (
    <div
      style={{
        height: 6,
        background: theme.bgTertiary,
        borderRadius: 3,
        overflow: "hidden",
        marginTop: 8,
      }}
    >
      <div
        style={{
          height: "100%",
          width: `${pct}%`,
          background: color,
          borderRadius: 3,
          transition: "width 0.5s",
        }}
      />
    </div>
  );
}

export default function RiskGauges({ vix, yields = [] }) {
  const { theme } = useTheme();
  const vixInfo = VIXLevel(vix);

  const us2y  = yields.find((y) => y.name === "US 2Y")?.yield;
  const us10y = yields.find((y) => y.name === "US 10Y")?.yield;
  const spread = us2y != null && us10y != null ? us10y - us2y : null;

  const spreadLabel =
    spread == null ? "N/A"
    : spread > 0.5  ? "Normal"
    : spread > 0    ? "Flat"
    : spread > -0.5 ? "Mild Inversion"
    : "Inverted";

  const spreadColor =
    spread == null ? theme.textMuted
    : spread > 0.5  ? theme.positive
    : spread > 0    ? theme.warning
    : theme.negative;

  return (
    <div
      style={{
        background: theme.bgCard,
        border: `1px solid ${theme.border}`,
        borderRadius: 10,
        padding: "14px 16px",
      }}
    >
      <div style={{ fontSize: 13, fontWeight: 600, color: theme.textPrimary, marginBottom: 16, letterSpacing: "0.03em" }}>
        Risk Indicators
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        {/* VIX */}
        <div>
          <div style={{ fontSize: 11, color: theme.textMuted, fontWeight: 500, letterSpacing: "0.05em" }}>
            VIX — CBOE Volatility
          </div>
          <div style={{ fontSize: 26, fontWeight: 700, color: vixInfo.color ? theme[vixInfo.color] : theme.textPrimary, marginTop: 4 }}>
            {vix != null ? vix.toFixed(2) : "—"}
          </div>
          <div style={{ fontSize: 12, color: vixInfo.color ? theme[vixInfo.color] : theme.textMuted, marginTop: 2 }}>
            {vixInfo.label}
          </div>
          {vix != null && (
            <GaugeBar value={vix} max={50} color={theme[vixInfo.color] || theme.textMuted} theme={theme} />
          )}
        </div>

        {/* 2s10s Spread */}
        <div>
          <div style={{ fontSize: 11, color: theme.textMuted, fontWeight: 500, letterSpacing: "0.05em" }}>
            2s10s Yield Spread
          </div>
          <div style={{ fontSize: 26, fontWeight: 700, color: spreadColor, marginTop: 4 }}>
            {spread != null ? `${spread > 0 ? "+" : ""}${(spread * 100).toFixed(0)}bp` : "—"}
          </div>
          <div style={{ fontSize: 12, color: spreadColor, marginTop: 2 }}>
            {spreadLabel}
          </div>
          {spread != null && (
            <GaugeBar
              value={Math.abs(spread) * 100}
              max={200}
              color={spreadColor}
              theme={theme}
            />
          )}
        </div>
      </div>
    </div>
  );
}
