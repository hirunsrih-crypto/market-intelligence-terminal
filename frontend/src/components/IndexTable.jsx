import { useTheme } from "../context/ThemeContext";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

const REGION_FLAGS = {
  US: "🇺🇸", TH: "🇹🇭", IN: "🇮🇳", IL: "🇮🇱", VN: "🇻🇳",
  JP: "🇯🇵", HK: "🇭🇰", KR: "🇰🇷", UK: "🇬🇧", DE: "🇩🇪",
  EU: "🇪🇺", CN: "🇨🇳",
};

function ChangeCell({ change, theme }) {
  if (change == null) return <span style={{ color: theme.textMuted }}>—</span>;
  const up = change > 0;
  const neutral = change === 0;
  return (
    <span
      style={{
        color: neutral ? theme.neutral : up ? theme.positive : theme.negative,
        display: "inline-flex",
        alignItems: "center",
        gap: 4,
        fontWeight: 500,
      }}
    >
      {neutral ? <Minus size={12} /> : up ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
      {up && "+"}
      {change.toFixed(2)}%
    </span>
  );
}

export default function IndexTable({ indices = [], title = "Global Equity Indices", filterRegion }) {
  const { theme } = useTheme();

  const rows = filterRegion
    ? indices.filter((i) => i.region === filterRegion)
    : indices;

  const colStyle = (align = "left") => ({
    padding: "10px 12px",
    textAlign: align,
    fontSize: 13,
    borderBottom: `1px solid ${theme.borderSubtle}`,
  });

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
          {title}
        </span>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: theme.bgTertiary }}>
            {["Index", "Value", "1D Change", "Region", "CCY"].map((h, i) => (
              <th
                key={h}
                style={{
                  ...colStyle(i > 0 ? "right" : "left"),
                  color: theme.textMuted,
                  fontWeight: 500,
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 && (
            <tr>
              <td colSpan={5} style={{ ...colStyle(), color: theme.textMuted, textAlign: "center", padding: 24 }}>
                Loading data...
              </td>
            </tr>
          )}
          {rows.map((row, idx) => (
            <tr
              key={row.ticker}
              style={{
                background: idx % 2 === 0 ? "transparent" : theme.bgTertiary + "40",
                transition: "background 0.15s",
              }}
            >
              <td style={colStyle()}>
                <div>
                  <span style={{ color: theme.textPrimary, fontWeight: 600, fontSize: 13 }}>{row.ticker}</span>
                  <span style={{ color: theme.textSecondary, fontSize: 11, display: "block" }}>{row.name}</span>
                </div>
              </td>
              <td style={{ ...colStyle("right"), color: theme.textPrimary, fontWeight: 500 }}>
                {row.value != null ? row.value.toLocaleString("en-US", { maximumFractionDigits: 2 }) : "—"}
              </td>
              <td style={{ ...colStyle("right") }}>
                <ChangeCell change={row.change} theme={theme} />
              </td>
              <td style={{ ...colStyle("right"), color: theme.textSecondary }}>
                <span style={{ fontSize: 16, marginRight: 4 }}>{REGION_FLAGS[row.region] || "🌐"}</span>
                {row.region}
              </td>
              <td style={{ ...colStyle("right") }}>
                <span
                  style={{
                    fontSize: 11,
                    color: theme.textMuted,
                    background: theme.tagBg,
                    borderRadius: 4,
                    padding: "2px 6px",
                  }}
                >
                  {row.currency}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
