import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import {
  clearAuthSession,
  fetchMe,
  getAccessToken,
  getStoredUser,
  loginUser,
  registerUser,
  storeAuthSession,
} from '../lib/api.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => getStoredUser());
  const [token, setToken] = useState(() => getAccessToken());
  const [checkingSession, setCheckingSession] = useState(Boolean(getAccessToken()));

  useEffect(() => {
    let active = true;
    async function validateSession() {
      if (!getAccessToken()) {
        setCheckingSession(false);
        return;
      }
      try {
        const currentUser = await fetchMe();
        if (!active) return;
        setUser(currentUser);
        setToken(getAccessToken());
        localStorage.setItem('lokerlens_user', JSON.stringify(currentUser));
      } catch {
        if (!active) return;
        clearAuthSession();
        setUser(null);
        setToken(null);
      } finally {
        if (active) setCheckingSession(false);
      }
    }
    validateSession();
    return () => {
      active = false;
    };
  }, []);

  async function login(payload) {
    const data = await loginUser(payload);
    storeAuthSession(data);
    setUser(data.user);
    setToken(data.access_token);
    return data.user;
  }

  async function register(payload) {
    return registerUser(payload);
  }

  function logout() {
    clearAuthSession();
    setUser(null);
    setToken(null);
  }

  const value = useMemo(
    () => ({
      user,
      token,
      isAuthenticated: Boolean(user && token),
      checkingSession,
      login,
      register,
      logout,
    }),
    [user, token, checkingSession],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider');
  }
  return context;
}
