import { Sun, Moon } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

export default function ThemeToggle() {
  const { isDark, toggleTheme, theme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      style={{
        padding: "6px 14px",
        borderRadius: "6px",
        fontSize: "12px",
        fontWeight: 500,
        background: theme.accentDim,
        border: `1px solid ${theme.accentBorder}`,
        color: theme.accent,
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 6,
        transition: "all 0.2s",
        letterSpacing: "0.02em",
      }}
    >
      {isDark ? <Sun size={13} /> : <Moon size={13} />}
      {isDark ? "Light" : "Dark"}
    </button>
  );
}
