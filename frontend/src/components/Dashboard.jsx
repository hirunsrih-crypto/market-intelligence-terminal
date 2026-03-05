import { useState } from "react";
import { useTheme } from "../context/ThemeContext";
import { useMarketData } from "../hooks/useMarketData";
import ThemeToggle from "./ThemeToggle";
import TickerStrip from "./TickerStrip";
import IndexTable from "./IndexTable";
import IntradayChart from "./IntradayChart";
import FXPanel from "./FXPanel";
import CommoditiesPanel from "./CommoditiesPanel";
import BondYields from "./BondYields";
import YieldCurve from "./YieldCurve";
import EcoCalendar from "./EcoCalendar";
import FundFlows from "./FundFlows";
import RiskGauges from "./RiskGauges";
import { RefreshCw, Activity } from "lucide-react";

const TABS = ["Overview", "Equity", "Fixed Income", "Macro & FX", "Fund Flows"];

const REGION_GROUPS = [
  { label: "Thailand",    region: "TH" },
  { label: "India",       region: "IN" },
  { label: "Israel",      region: "IL" },
  { label: "Vietnam",     region: "VN" },
  { label: "US",          region: "US" },
  { label: "Japan / HK / KR", region: null, regions: ["JP", "HK", "KR"] },
  { label: "Europe",      region: null, regions: ["UK", "DE", "EU"] },
  { label: "China",       region: "CN" },
];

export default function Dashboard() {
  const { theme } = useTheme();
  const { data, loading, error, lastUpdated, refresh } = useMarketData();
  const [activeTab, setActiveTab] = useState("Overview");

  const indices     = data?.indices     || [];
  const fx          = data?.fx          || [];
  const commodities = data?.commodities || [];
  const yields      = data?.yields      || [];
  const vix         = data?.vix;
  const calendar    = data?.calendar    || [];
  const flows       = data?.flows       || {};
  const intraday    = data?.intraday    || {};
  const crypto      = data?.crypto      || [];

  const headerStyle = {
    background: theme.bgHeader,
    borderBottom: `1px solid ${theme.border}`,
    position: "sticky",
    top: 0,
    zIndex: 100,
    backdropFilter: "blur(12px)",
  };

  const tabStyle = (active) => ({
    padding: "8px 16px",
    fontSize: 13,
    fontWeight: active ? 600 : 400,
    color: active ? theme.accent : theme.textSecondary,
    borderBottom: `2px solid ${active ? theme.accent : "transparent"}`,
    cursor: "pointer",
    background: "transparent",
    border: "none",
    borderBottom: `2px solid ${active ? theme.accent : "transparent"}`,
    transition: "all 0.15s",
    letterSpacing: "0.02em",
  });

  const section = (children) => (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>{children}</div>
  );

  const grid = (cols, children) => (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
        gap: 20,
      }}
    >
      {children}
    </div>
  );

  return (
    <div style={{ minHeight: "100vh", background: theme.bgPrimary, color: theme.textPrimary }}>
      {/* Header */}
      <div style={headerStyle}>
        <div style={{ maxWidth: 1600, margin: "0 auto", padding: "12px 24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <Activity size={18} color={theme.accent} />
              <span style={{ fontWeight: 700, fontSize: 15, color: theme.textPrimary, letterSpacing: "0.04em" }}>
                MARKET INTELLIGENCE TERMINAL
              </span>
              <span
                style={{
                  fontSize: 10,
                  color: theme.accent,
                  background: theme.accentDim,
                  border: `1px solid ${theme.accentBorder}`,
                  padding: "2px 7px",
                  borderRadius: 4,
                  letterSpacing: "0.05em",
                  fontWeight: 600,
                }}
              >
                DAOL INVESTMENT
              </span>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              {lastUpdated && (
                <span style={{ fontSize: 11, color: theme.textMuted }}>
                  Updated {lastUpdated}
                </span>
              )}
              <button
                onClick={refresh}
                style={{
                  background: "transparent",
                  border: `1px solid ${theme.border}`,
                  borderRadius: 6,
                  padding: "5px 8px",
                  color: theme.textSecondary,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <RefreshCw size={13} />
              </button>
              <ThemeToggle />
            </div>
          </div>

          <div style={{ display: "flex", gap: 0, borderBottom: `1px solid ${theme.border}` }}>
            {TABS.map((tab) => (
              <button key={tab} style={tabStyle(activeTab === tab)} onClick={() => setActiveTab(tab)}>
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Ticker Strip */}
      <TickerStrip indices={indices} fx={fx} commodities={commodities} />

      {/* Loading / Error */}
      {loading && (
        <div style={{ textAlign: "center", padding: 60, color: theme.textMuted, fontSize: 14 }}>
          Loading market data...
        </div>
      )}
      {error && (
        <div
          style={{
            margin: "16px 24px",
            padding: "12px 16px",
            background: "rgba(248,113,113,0.1)",
            border: "1px solid rgba(248,113,113,0.3)",
            borderRadius: 8,
            color: theme.negative,
            fontSize: 13,
          }}
        >
          Backend offline — showing cached or sample data. Error: {error}
        </div>
      )}

      {/* Main Content */}
      <div style={{ maxWidth: 1600, margin: "0 auto", padding: "24px 24px" }}>

        {/* OVERVIEW TAB */}
        {activeTab === "Overview" && section(
          <>
            {grid(3,
              <>
                <IntradayChart intraday={intraday} />
                <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
                  <RiskGauges vix={vix} yields={yields} />
                  <FXPanel fx={fx.slice(0, 5)} />
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
                  <CommoditiesPanel commodities={commodities} />
                </div>
              </>
            )}
            <IndexTable indices={indices} title="Global Equity Indices — Overview" />
            <EcoCalendar events={calendar} />
          </>
        )}

        {/* EQUITY TAB */}
        {activeTab === "Equity" && section(
          <>
            <IntradayChart intraday={intraday} />
            {grid(2,
              <>
                <IndexTable indices={indices.filter((i) => ["TH"].includes(i.region))} title="Thailand" />
                <IndexTable indices={indices.filter((i) => ["IN"].includes(i.region))} title="India" />
              </>
            )}
            {grid(2,
              <>
                <IndexTable indices={indices.filter((i) => ["IL"].includes(i.region))} title="Israel" />
                <IndexTable indices={indices.filter((i) => ["VN"].includes(i.region))} title="Vietnam" />
              </>
            )}
            {grid(2,
              <>
                <IndexTable indices={indices.filter((i) => ["US"].includes(i.region))} title="United States" />
                <IndexTable indices={indices.filter((i) => ["JP","HK","KR"].includes(i.region))} title="Japan / HK / Korea" />
              </>
            )}
            {grid(2,
              <>
                <IndexTable indices={indices.filter((i) => ["UK","DE","EU"].includes(i.region))} title="Europe" />
                <IndexTable indices={indices.filter((i) => ["CN"].includes(i.region))} title="China" />
              </>
            )}
          </>
        )}

        {/* FIXED INCOME TAB */}
        {activeTab === "Fixed Income" && section(
          <>
            <RiskGauges vix={vix} yields={yields} />
            {grid(2,
              <>
                <BondYields yields={yields} />
                <YieldCurve yields={yields} />
              </>
            )}
          </>
        )}

        {/* MACRO & FX TAB */}
        {activeTab === "Macro & FX" && section(
          <>
            {grid(2,
              <>
                <FXPanel fx={fx} />
                <CommoditiesPanel commodities={commodities} />
              </>
            )}
            {/* Crypto row */}
            <div
              style={{
                background: theme.bgCard,
                border: `1px solid ${theme.border}`,
                borderRadius: 10,
                padding: "14px 16px",
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 600, color: theme.textPrimary, marginBottom: 12, letterSpacing: "0.03em" }}>
                Crypto
              </div>
              <div style={{ display: "flex", gap: 16 }}>
                {crypto.map((c) => {
                  const up = c.change >= 0;
                  return (
                    <div
                      key={c.ticker}
                      style={{
                        background: theme.bgTertiary,
                        border: `1px solid ${theme.border}`,
                        borderRadius: 8,
                        padding: "10px 16px",
                        minWidth: 140,
                      }}
                    >
                      <div style={{ fontSize: 11, color: theme.textMuted }}>{c.name}</div>
                      <div style={{ fontSize: 20, fontWeight: 700, color: theme.crypto, marginTop: 4 }}>
                        ${c.value != null ? c.value.toLocaleString("en-US", { maximumFractionDigits: 0 }) : "—"}
                      </div>
                      <div style={{ fontSize: 12, color: up ? theme.positive : theme.negative, marginTop: 2 }}>
                        {c.change != null ? `${up ? "+" : ""}${c.change.toFixed(2)}%` : "—"}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <EcoCalendar events={calendar} />
          </>
        )}

        {/* FUND FLOWS TAB */}
        {activeTab === "Fund Flows" && section(
          <>
            <FundFlows flows={flows} />
          </>
        )}
      </div>
    </div>
  );
}
