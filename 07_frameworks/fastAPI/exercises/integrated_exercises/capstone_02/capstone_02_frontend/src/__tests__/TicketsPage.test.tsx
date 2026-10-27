import { render, screen, waitFor } from '@testing-library/react';
import TicketsPage from '../pages/TicketsPage';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../contexts/AuthContext';
import { ToastProvider } from '../components/feedback/ToastContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect } from 'vitest';
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false }
  }
});

const Wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    <ToastProvider>
      <AuthProvider>
        <MemoryRouter>{children}</MemoryRouter>
      </AuthProvider>
    </ToastProvider>
  </QueryClientProvider>
);

describe('TicketsPage Error & Empty States', () => {
  it('should display empty ticket-list state when no tickets exist', async () => {
    // Override API to return 0 tickets
    server.use(
      http.get('*/tickets', () => {
        return HttpResponse.json({ items: [], page: 1, page_size: 10, total: 0, total_pages: 0 });
      })
    );

    render(<TicketsPage />, { wrapper: Wrapper });
    
    await waitFor(() => {
      expect(screen.getByText(/No tickets found/i)).toBeInTheDocument();
    });
  });

  it('should display API error handling message', async () => {
    // Override API to return 500
    server.use(
      http.get('*/tickets', () => {
        return new HttpResponse(null, { status: 500 });
      })
    );

    render(<TicketsPage />, { wrapper: Wrapper });
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to load tickets/i)).toBeInTheDocument();
    });
  });
});
