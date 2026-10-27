import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from '../routes/ProtectedRoute';
import { AuthProvider } from '../contexts/AuthContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false }
  }
});

const ProtectedContent = () => <div>Protected Dashboard</div>;
const LoginContent = () => <div>Login Page</div>;

describe('ProtectedRoute', () => {
  it('should redirect to login if not authenticated', async () => {
    // Clear localStorage token
    localStorage.removeItem('access_token');
    
    render(
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <MemoryRouter initialEntries={['/dashboard']}>
            <Routes>
              <Route path="/login" element={<LoginContent />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/dashboard" element={<ProtectedContent />} />
              </Route>
            </Routes>
          </MemoryRouter>
        </AuthProvider>
      </QueryClientProvider>
    );

    // Initial state will be Loading because AuthProvider fetches /auth/me if there is a token.
    // Wait, without token it should not fetch /auth/me and immediately set isLoading to false.
    // And user is null, so it redirects to /login.
    
    const loginText = await screen.findByText('Login Page');
    expect(loginText).toBeInTheDocument();
    expect(screen.queryByText('Protected Dashboard')).not.toBeInTheDocument();
  });
});
