import type { User, Ticket, TicketComment } from '../types/domain';

export interface MockCredential {
  email: string;
  passwordHash: string; // Plaintext for mock simplicity
}

export const mockUsers: User[] = [
  {
    id: 1,
    name: "Customer Demo",
    email: "customer@example.com",
    role: "customer",
    is_active: true,
    created_at: "2026-09-11T12:00:00Z"
  },
  {
    id: 2,
    name: "Agent Demo",
    email: "agent@example.com",
    role: "agent",
    is_active: true,
    created_at: "2026-09-11T12:00:00Z"
  },
  {
    id: 3,
    name: "Admin Demo",
    email: "admin@example.com",
    role: "admin",
    is_active: true,
    created_at: "2026-09-11T12:00:00Z"
  }
];

export const mockCredentials: MockCredential[] = [
  { email: "customer@example.com", passwordHash: "customer123" },
  { email: "agent@example.com", passwordHash: "agent123" },
  { email: "admin@example.com", passwordHash: "admin123" }
];

export const mockTickets: Ticket[] = [
  {
    id: 1,
    title: "Computer does not start",
    description: "The computer shows no sign of power.",
    status: "open",
    priority: "high",
    category: "hardware",
    created_by: mockUsers[0], // Customer
    assigned_to: null,
    created_at: "2026-09-11T12:00:00Z",
    updated_at: "2026-09-11T12:00:00Z"
  },
  {
    id: 2,
    title: "Cannot access email",
    description: "Password reset is not working and I am locked out.",
    status: "in_progress",
    priority: "urgent",
    category: "access",
    created_by: mockUsers[0],
    assigned_to: mockUsers[1], // Agent
    created_at: "2026-09-10T09:30:00Z",
    updated_at: "2026-09-11T14:20:00Z"
  }
];

export interface MockTicketComment extends TicketComment {
  ticket_id: number;
}

export let mockComments: MockTicketComment[] = [
  {
    id: 1,
    content: "We are investigating the problem.",
    author: mockUsers[1],
    created_at: "2026-09-11T13:00:00Z",
    ticket_id: 1
  }
];

// Simple in-memory db that can be mutated in runtime
export const db = {
  users: [...mockUsers],
  credentials: [...mockCredentials],
  tickets: [...mockTickets],
  comments: [...mockComments]
};
