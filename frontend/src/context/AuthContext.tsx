import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import axios from '../utils/axios';

interface AuthState {
  token: string | null;
  username: string | null;
  age: number | null;
}

interface AuthContextType extends AuthState {
  login: (token: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [username, setUsername] = useState<string | null>(null);
  const [age, setAge] = useState<number | null>(null);

  const logout = useCallback(async () => {
    // Call backend logout endpoint if we have a token
    if (token) {
      try {
        await axios.post('/api/auth/logout', {}, { 
          headers: { Authorization: `Bearer ${token}` } 
        });
      } catch (error) {
        // Continue with logout even if backend call fails
        console.warn('Backend logout failed:', error);
      }
    }
    
    // Clear frontend state and storage
    localStorage.removeItem('token');
    setToken(null);
    setUsername(null);
    setAge(null);
  }, [token]);

  useEffect(() => {
    if (token) {
      axios.get('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
        .then(res => {
          setUsername(res.data.username);
          setAge(res.data.age ?? null);
        })
        .catch(() => logout());
    }
  }, [token, logout]);

  const login = async (t: string) => {
    localStorage.setItem('token', t);
    setToken(t);
  };

  return (
    <AuthContext.Provider value={{ token, username, age, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
