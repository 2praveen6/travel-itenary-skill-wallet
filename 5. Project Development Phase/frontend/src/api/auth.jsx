import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "./client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(!token);

  useEffect(() => {
    if (!token) {
      setUser(null);
      setReady(true);
      return;
    }
    api("/api/auth/me", { token })
      .then((data) => setUser(data.user))
      .catch(() => {
        localStorage.removeItem("token");
        setToken(null);
      })
      .finally(() => setReady(true));
  }, [token]);

  const value = useMemo(
    () => ({
      token,
      user,
      ready,
      async login(email, password) {
        const data = await api("/api/auth/login", { method: "POST", body: { email, password } });
        localStorage.setItem("token", data.token);
        setToken(data.token);
        setUser(data.user);
      },
      async register(name, email, password) {
        const data = await api("/api/auth/register", { method: "POST", body: { name, email, password } });
        localStorage.setItem("token", data.token);
        setToken(data.token);
        setUser(data.user);
      },
      logout() {
        localStorage.removeItem("token");
        setToken(null);
        setUser(null);
      },
    }),
    [token, user, ready]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
