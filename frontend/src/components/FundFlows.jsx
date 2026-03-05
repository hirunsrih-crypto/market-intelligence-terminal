import { useTheme } from "../context/ThemeContext";
import { TrendingUp, TrendingDown } from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from "recharts";

const REGION_FLAGS = {
  TH: "🇹🇭", IN: "🇮🇳", VN: "🇻🇳", IL: "🇮🇱",
};

export default function FundFlows({ flows = {} }) {
  const { theme } = useTheme();
  const markets = flows.markets || [];

  const chartData = markets.map((m) => ({
    name: m.region,
    value: m.foreign_net,
  }));

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
          Foreign Fund Flows
        </span>
        {flows.date && (
          <span style={{ fontSize: 11, color: theme.textMuted, marginLeft: 8 }}>
            {flows.date}
          </span>
        )}
      </div>

      <div style={{ padding: "12px 16px" }}>
        {markets.length > 0 && (
          <div style={{ height: 140, marginBottom: 16 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.gridStroke} />
                <XAxis dataKey="name" tick={{ fill: theme.textMuted, fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: theme.textMuted, fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    background: theme.tooltipBg,
                    border: `1px solid ${theme.tooltipBorder}`,
                    borderRadius: 6,
                    fontSize: 12,
                    color: theme.textPrimary,
                  }}
                  formatter={(v) => [v.toLocaleString(), "Net Flow"]}
                />
                <Bar dataKey="value" radius={[3, 3, 0, 0]}>
                  {chartData.map((entry, idx) => (
                    <Cell
                      key={idx}
                      fill={entry.value >= 0 ? theme.positive : theme.negative}
                      fillOpacity={0.8}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {markets.map((m) => {
            const up = m.foreign_net >= 0;
            return (
              <div
                key={m.region}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "8px 12px",
                  background: theme.bgTertiary,
                  borderRadius: 7,
                  border: `1px solid ${theme.border}`,
                }}
              >
                <div>
                  <span style={{ fontSize: 13, color: theme.textPrimary, fontWeight: 500 }}>
                    {REGION_FLAGS[m.region] || "🌐"} {m.market}
                  </span>
                  <span style={{ fontSize: 11, color: theme.textMuted, marginLeft: 6 }}>{m.note}</span>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div
                    style={{
                      fontSize: 13,
                      fontWeight: 600,
                      color: up ? theme.positive : theme.negative,
                      display: "flex",
                      alignItems: "center",
                      gap: 4,
                    }}
                  >
                    {up ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                    {up ? "+" : ""}
                    {m.foreign_net.toLocaleString()} {m.unit}
                  </div>
                  <div style={{ fontSize: 10, color: theme.textMuted }}>
                    B: {m.foreign_buy.toLocaleString()} / S: {m.foreign_sell.toLocaleString()}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {flows.global && (
          <div
            style={{
              marginTop: 12,
              padding: "10px 12px",
              background: theme.accentDim,
              border: `1px solid ${theme.accentBorder}`,
              borderRadius: 7,
            }}
          >
            <div style={{ fontSize: 11, color: theme.accent, fontWeight: 600, marginBottom: 6 }}>
              Global Flows ({flows.global.source})
            </div>
            <div style={{ display: "flex", gap: 20 }}>
              {[
                { label: "EM Equity", value: flows.global.em_equity_flows },
                { label: "DM Equity", value: flows.global.dm_equity_flows },
                { label: "Bonds",     value: flows.global.bond_flows },
              ].map((g) => {
                const up = g.value >= 0;
                return (
                  <div key={g.label}>
                    <div style={{ fontSize: 10, color: theme.textMuted }}>{g.label}</div>
                    <div style={{ fontSize: 12, fontWeight: 600, color: up ? theme.positive : theme.negative }}>
                      {up ? "+" : ""}{g.value.toLocaleString()} {flows.global.unit}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
