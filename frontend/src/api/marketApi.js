import axios from "axios";

const BASE = import.meta.env.VITE_API_URL || "";

export const api = {
  getMarketData:  () => axios.get(`${BASE}/api/market-data`).then((r) => r.data),
  getIntraday:    (sym) => axios.get(`${BASE}/api/intraday/${sym}`).then((r) => r.data),
  getYieldCurve:  () => axios.get(`${BASE}/api/yield-curve`).then((r) => r.data),
  getEcoCalendar: () => axios.get(`${BASE}/api/eco-calendar`).then((r) => r.data),
  getFundFlows:   () => axios.get(`${BASE}/api/fund-flows`).then((r) => r.data),
  getHealth:      () => axios.get(`${BASE}/api/health`).then((r) => r.data),
};
