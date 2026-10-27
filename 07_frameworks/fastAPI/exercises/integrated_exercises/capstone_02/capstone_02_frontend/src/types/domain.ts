export type UserRole = "customer" | "agent" | "admin";

export type TicketStatus =
  | "open"
  | "in_progress"
  | "waiting_customer"
  | "resolved"
  | "closed";

export type TicketPriority =
  | "low"
  | "medium"
  | "high"
  | "urgent";

export type TicketCategory =
  | "hardware"
  | "software"
  | "network"
  | "access"
  | "other";

export interface UserSummary {
  id: number;
  name: string;
  email: string;
  role: UserRole;
}

export interface User extends UserSummary {
  is_active: boolean;
  created_at: string;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  category: TicketCategory;
  created_by: UserSummary;
  assigned_to: UserSummary | null;
  created_at: string;
  updated_at: string;
}

export interface TicketComment {
  id: number;
  content: string;
  author: UserSummary;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface DashboardSummary {
  total_tickets: number;
  open_tickets: number;
  in_progress_tickets: number;
  waiting_customer_tickets: number;
  resolved_tickets: number;
  closed_tickets: number;
  urgent_tickets: number;
  my_assigned_tickets: number;
}
