import { render, screen } from '@testing-library/react';
import { Badge } from '../components/ui/Badge';
import { describe, it, expect } from 'vitest';

describe('Badge Component & Conversions', () => {
  it('should render correct priority badge', () => {
    const { rerender } = render(<Badge variant="destructive">Urgent</Badge>);
    let badge = screen.getByText('Urgent');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-destructive');

    rerender(<Badge variant="secondary">Medium</Badge>);
    badge = screen.getByText('Medium');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-secondary');
  });
  
  it('should render correct status badge variants', () => {
    const { rerender } = render(<Badge variant="warning">Waiting for Customer</Badge>);
    expect(screen.getByText('Waiting for Customer')).toBeInTheDocument();

    rerender(<Badge variant="success">Resolved</Badge>);
    let badge = screen.getByText('Resolved');
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass('bg-green-500/15');
  });
});
