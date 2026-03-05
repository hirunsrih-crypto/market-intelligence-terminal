import { useTheme } from "../context/ThemeContext";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine,
} from "recharts";

export default function YieldCurve({ yields = [] }) {
  const { theme } = useTheme();
  const sorted = [...yields].sort((a, b) => (a.maturity || 0) - (b.maturity || 0));

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
          US Yield Curve
        </span>
      </div>
      <div style={{ padding: "16px 8px 8px" }}>
        {sorted.length === 0 ? (
          <div style={{ height: 160, display: "flex", alignItems: "center", justifyContent: "center", color: theme.textMuted, fontSize: 13 }}>
            Yield data unavailable
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={160}>
            <LineChart data={sorted} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.gridStroke} />
              <XAxis dataKey="name" tick={{ fill: theme.textMuted, fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: theme.textMuted, fontSize: 10 }} axisLine={false} tickLine={false} domain={["auto", "auto"]} />
              <Tooltip
                contentStyle={{
                  background: theme.tooltipBg,
                  border: `1px solid ${theme.tooltipBorder}`,
                  borderRadius: 6,
                  fontSize: 12,
                  color: theme.textPrimary,
                }}
                formatter={(v) => [`${v.toFixed(3)}%`, "Yield"]}
              />
              <Line type="monotone" dataKey="yield" stroke={theme.accent} strokeWidth={2} dot={{ fill: theme.accent, r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
