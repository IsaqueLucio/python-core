import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User } from '../types/domain';
import { getMe, login as apiLogin, register as apiRegister } from '../api/auth';
import { useQuery, useQueryClient } from '@tanstack/react-query';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: unknown) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
  const queryClient = useQueryClient();

  const { data: user, isLoading, refetch } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: getMe,
    enabled: !!token,
    retry: false,
  });

  useEffect(() => {
    const handleUnauthorized = () => {
      setToken(null);
      queryClient.setQueryData(['auth', 'me'], null);
      queryClient.clear();
    };

    window.addEventListener('auth-unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth-unauthorized', handleUnauthorized);
  }, [queryClient]);

  const login = async (username: string, password: string) => {
    const data = await apiLogin(username, password);
    localStorage.setItem('access_token', data.access_token);
    setToken(data.access_token);
    await refetch();
  };

  const register = async (data: unknown) => {
    await apiRegister(data as Record<string, unknown>);
    // After registration, login is required
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    queryClient.setQueryData(['auth', 'me'], null);
    queryClient.clear();
  };

  return (
    <AuthContext.Provider value={{
      user: user || null,
      isLoading,
      login,
      register,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
