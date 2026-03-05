import { useTheme } from "../context/ThemeContext";

const COUNTRY_FLAGS = {
  US: "🇺🇸", TH: "🇹🇭", IN: "🇮🇳", IL: "🇮🇱", VN: "🇻🇳",
  EU: "🇪🇺", JP: "🇯🇵", CN: "🇨🇳", UK: "🇬🇧", KR: "🇰🇷",
};

function ImpactDot({ impact, theme }) {
  const bg =
    impact === "high"   ? theme.impactHighText
    : impact === "medium" ? theme.impactMedText
    : theme.impactLowText;

  return (
    <span
      style={{
        display: "inline-block",
        width: 8,
        height: 8,
        borderRadius: "50%",
        background: bg,
        flexShrink: 0,
        marginTop: 3,
      }}
    />
  );
}

export default function EcoCalendar({ events = [] }) {
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
          Economic Calendar — Today
        </span>
      </div>

      <div style={{ maxHeight: 380, overflowY: "auto" }}>
        {events.length === 0 && (
          <div style={{ padding: "24px 16px", color: theme.textMuted, textAlign: "center", fontSize: 13 }}>
            No events scheduled today
          </div>
        )}
        {events.map((ev, idx) => {
          const released = ev.actual && ev.actual !== "-" && ev.actual !== "—";
          return (
            <div
              key={idx}
              style={{
                display: "grid",
                gridTemplateColumns: "52px 16px 1fr 80px 80px 80px",
                gap: 10,
                alignItems: "start",
                padding: "11px 16px",
                borderBottom: `1px solid ${theme.borderSubtle}`,
                background: released ? theme.accentBg + "30" : "transparent",
              }}
            >
              <span style={{ fontSize: 12, color: theme.textMuted, fontWeight: 500 }}>{ev.time}</span>
              <ImpactDot impact={ev.impact} theme={theme} />
              <div>
                <span style={{ fontSize: 13, color: theme.textPrimary, fontWeight: 500 }}>
                  {COUNTRY_FLAGS[ev.country] || "🌐"} {ev.event}
                </span>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 10, color: theme.textMuted }}>Actual</div>
                <div
                  style={{
                    fontSize: 13,
                    fontWeight: 600,
                    color: released ? theme.positive : theme.textSecondary,
                  }}
                >
                  {ev.actual || "—"}
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 10, color: theme.textMuted }}>Forecast</div>
                <div style={{ fontSize: 13, color: theme.textSecondary }}>{ev.forecast || "—"}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 10, color: theme.textMuted }}>Previous</div>
                <div style={{ fontSize: 13, color: theme.textSecondary }}>{ev.previous || "—"}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
