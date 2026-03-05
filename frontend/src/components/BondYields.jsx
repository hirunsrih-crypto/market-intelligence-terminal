import { useTheme } from "../context/ThemeContext";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

export default function BondYields({ yields = [] }) {
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
          US Treasury Yields
        </span>
      </div>

      <div style={{ padding: "12px 16px 8px" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(100px, 1fr))", gap: 12, marginBottom: 16 }}>
          {yields.map((y) => {
            const up = y.change >= 0;
            return (
              <div
                key={y.name}
                style={{
                  background: theme.bgTertiary,
                  borderRadius: 8,
                  padding: "10px 12px",
                  border: `1px solid ${theme.border}`,
                }}
              >
                <div style={{ fontSize: 11, color: theme.textMuted, fontWeight: 500 }}>{y.name}</div>
                <div style={{ fontSize: 16, fontWeight: 700, color: theme.textPrimary, marginTop: 4 }}>
                  {y.yield != null ? `${y.yield.toFixed(3)}%` : "—"}
                </div>
                <div style={{ fontSize: 11, color: up ? theme.positive : theme.negative, marginTop: 2 }}>
                  {y.change != null ? `${up ? "+" : ""}${y.change.toFixed(3)}` : "—"}
                </div>
              </div>
            );
          })}
        </div>

        {sorted.length > 0 && (
          <div style={{ height: 120 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={sorted} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.gridStroke} />
                <XAxis
                  dataKey="name"
                  tick={{ fill: theme.textMuted, fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: theme.textMuted, fontSize: 10 }}
                  axisLine={false}
                  tickLine={false}
                  domain={["auto", "auto"]}
                />
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
                <Line
                  type="monotone"
                  dataKey="yield"
                  stroke={theme.accent}
                  strokeWidth={2}
                  dot={{ fill: theme.accent, r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
