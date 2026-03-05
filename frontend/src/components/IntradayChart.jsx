import { useTheme } from "../context/ThemeContext";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { useState } from "react";

const CHART_COLORS = {
  SPX:     "chartSPX",
  SET:     "chartSET",
  NIFTY:   "chartNIFTY",
  VNINDEX: "chartVN",
};

const CHART_LABELS = {
  SPX: "S&P 500", SET: "SET Index", NIFTY: "Nifty 50", VNINDEX: "VN-Index",
};

export default function IntradayChart({ intraday = {} }) {
  const { theme } = useTheme();
  const symbols = Object.keys(intraday).filter((k) => (intraday[k] || []).length > 0);
  const [active, setActive] = useState(symbols[0] || "SPX");

  const bars = intraday[active] || [];
  const colorKey = CHART_COLORS[active] || "chartSPX";
  const color = theme[colorKey];

  const prices = bars.map((b) => b.price).filter(Boolean);
  const minPrice = prices.length ? Math.min(...prices) * 0.998 : 0;
  const maxPrice = prices.length ? Math.max(...prices) * 1.002 : 1;

  const subsample = bars.filter((_, i) => i % 3 === 0);

  return (
    <div
      style={{
        background: theme.bgCard,
        border: `1px solid ${theme.border}`,
        borderRadius: 10,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "14px 16px",
          borderBottom: `1px solid ${theme.border}`,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span style={{ fontSize: 13, fontWeight: 600, color: theme.textPrimary, letterSpacing: "0.03em" }}>
          Intraday Chart — {CHART_LABELS[active] || active}
        </span>
        <div style={{ display: "flex", gap: 6 }}>
          {symbols.map((sym) => (
            <button
              key={sym}
              onClick={() => setActive(sym)}
              style={{
                padding: "4px 10px",
                borderRadius: 5,
                fontSize: 11,
                fontWeight: 500,
                cursor: "pointer",
                border: `1px solid ${active === sym ? theme.accentBorder : theme.border}`,
                background: active === sym ? theme.accentDim : "transparent",
                color: active === sym ? theme.accent : theme.textSecondary,
                transition: "all 0.15s",
              }}
            >
              {sym}
            </button>
          ))}
        </div>
      </div>

      <div style={{ padding: "16px 8px 8px" }}>
        {bars.length === 0 ? (
          <div style={{ height: 180, display: "flex", alignItems: "center", justifyContent: "center", color: theme.textMuted, fontSize: 13 }}>
            No intraday data available
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={subsample} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id={`grad-${active}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor={color} stopOpacity={0.2} />
                  <stop offset="95%" stopColor={color} stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.gridStroke} />
              <XAxis
                dataKey="time"
                tick={{ fill: theme.textMuted, fontSize: 10 }}
                axisLine={false}
                tickLine={false}
                interval="preserveStartEnd"
              />
              <YAxis
                domain={[minPrice, maxPrice]}
                tick={{ fill: theme.textMuted, fontSize: 10 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v) => v.toLocaleString("en-US", { maximumFractionDigits: 0 })}
              />
              <Tooltip
                contentStyle={{
                  background: theme.tooltipBg,
                  border: `1px solid ${theme.tooltipBorder}`,
                  borderRadius: 6,
                  fontSize: 12,
                  color: theme.textPrimary,
                }}
                formatter={(v) => [v.toLocaleString("en-US", { maximumFractionDigits: 2 }), "Price"]}
              />
              <Area
                type="monotone"
                dataKey="price"
                stroke={color}
                strokeWidth={1.5}
                fill={`url(#grad-${active})`}
                dot={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
