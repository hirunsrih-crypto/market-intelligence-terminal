import { createContext, useContext, useState, useEffect } from "react";
import { darkTheme } from "../themes/dark";
import { lightTheme } from "../themes/light";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [isDark, setIsDark] = useState(() => {
    const saved = localStorage.getItem("mit-theme");
    return saved ? saved === "dark" : true;
  });

  const theme = isDark ? darkTheme : lightTheme;

  useEffect(() => {
    localStorage.setItem("mit-theme", isDark ? "dark" : "light");
    document.body.style.backgroundColor = theme.bgPrimary;
  }, [isDark, theme.bgPrimary]);

  const toggleTheme = () => setIsDark((prev) => !prev);

  return (
    <ThemeContext.Provider value={{ theme, isDark, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => useContext(ThemeContext);
