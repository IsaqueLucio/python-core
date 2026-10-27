import { http, HttpResponse } from 'msw';
import { db } from './db';
import type { User, Ticket, DashboardSummary } from '../types/domain';
import type { MockTicketComment } from './db';

const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Helper to authenticate requests and reject inactive users
const getUserFromToken = (request: Request) => {
  const authHeader = request.headers.get('Authorization');
  if (!authHeader || !authHeader.startsWith('Bearer ')) return null;
  const token = authHeader.split(' ')[1];
  const user = db.users.find(u => `mock-jwt-token-${u.id}` === token);
  if (!user || !user.is_active) return null;
  return user;
};

// Permission Helpers
const canViewTicket = (user: User, ticket: Ticket) => {
  if (user.role === 'admin') return true;
  if (user.role === 'customer') return ticket.created_by.id === user.id;
  if (user.role === 'agent') return ticket.assigned_to === null || ticket.assigned_to.id === user.id;
  return false;
};

const canEditTicket = (user: User, ticket: Ticket) => {
  if (user.role === 'admin') return true;
  if (user.role === 'customer') return ticket.created_by.id === user.id && ticket.status === 'open';
  if (user.role === 'agent') return ticket.assigned_to?.id === user.id;
  return false;
};

const canDeleteTicket = (user: User, ticket: Ticket) => {
  if (user.role === 'admin') return true;
  if (user.role === 'customer') return ticket.created_by.id === user.id && ticket.status === 'open';
  return false;
};

export const handlers = [
  // ========================
  // AUTH ENDPOINTS
  // ========================

  http.post(`${API_URL}/auth/login`, async ({ request }) => {
    const text = await request.text();
    const params = new URLSearchParams(text);
    const username = params.get('username');
    const password = params.get('password');

    const cred = db.credentials.find(c => c.email === username);
    if (!cred || cred.passwordHash !== password) {
      return HttpResponse.json({ detail: "Invalid email or password" }, { status: 401 });
    }

    const user = db.users.find(u => u.email === username);
    if (!user || !user.is_active) {
      return HttpResponse.json({ detail: "User is inactive" }, { status: 401 });
    }

    return HttpResponse.json({
      access_token: `mock-jwt-token-${user.id}`,
      token_type: "bearer"
    });
  }),

  http.post(`${API_URL}/auth/register`, async ({ request }) => {
    const data = await request.json() as unknown as Record<string, unknown>;
    
    if (db.users.find(u => u.email === data.email)) {
      return HttpResponse.json({ detail: "Email already registered" }, { status: 409 });
    }

    const newUser: User = {
      id: db.users.length > 0 ? Math.max(...db.users.map(u => u.id)) + 1 : 1,
      name: data.name as string,
      email: data.email as string,
      role: "customer",
      is_active: true,
      created_at: new Date().toISOString()
    };
    
    db.users.push(newUser);
    db.credentials.push({ email: data.email as string, passwordHash: data.password as string });

    return HttpResponse.json(newUser, { status: 201 });
  }),

  http.get(`${API_URL}/auth/me`, async ({ request }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });
    return HttpResponse.json(user);
  }),

  // ========================
  // TICKETS ENDPOINTS
  // ========================

  http.get(`${API_URL}/tickets`, async ({ request }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const url = new URL(request.url);
    const page = parseInt(url.searchParams.get('page') || '1');
    const pageSize = parseInt(url.searchParams.get('page_size') || '10');
    const status = url.searchParams.get('status');
    const priority = url.searchParams.get('priority');
    const category = url.searchParams.get('category');
    const search = url.searchParams.get('search')?.toLowerCase();
    const assignedToMe = url.searchParams.get('assigned_to_me') === 'true';

    let tickets = db.tickets.filter(t => canViewTicket(user, t));

    if (status) tickets = tickets.filter(t => t.status === status);
    if (priority) tickets = tickets.filter(t => t.priority === priority);
    if (category) tickets = tickets.filter(t => t.category === category);
    if (assignedToMe) tickets = tickets.filter(t => t.assigned_to?.id === user.id);
    if (search) tickets = tickets.filter(t => 
      t.title.toLowerCase().includes(search) || t.description.toLowerCase().includes(search)
    );

    // Sort: created_at DESC, id DESC
    tickets.sort((a, b) => {
      const dateA = new Date(a.created_at).getTime();
      const dateB = new Date(b.created_at).getTime();
      if (dateA !== dateB) return dateB - dateA;
      return b.id - a.id;
    });

    const total = tickets.length;
    const items = tickets.slice((page - 1) * pageSize, page * pageSize);

    return HttpResponse.json({
      items,
      page,
      page_size: pageSize,
      total,
      total_pages: Math.ceil(total / pageSize)
    });
  }),

  http.get(`${API_URL}/tickets/:id`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const ticket = db.tickets.find(t => t.id === parseInt(params.id as string));
    if (!ticket) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });

    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    return HttpResponse.json(ticket);
  }),

  http.post(`${API_URL}/tickets`, async ({ request }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const data = await request.json() as unknown as Record<string, unknown>;
    
    const newTicket: Ticket = {
      id: db.tickets.length > 0 ? Math.max(...db.tickets.map(t => t.id)) + 1 : 1,
      title: data.title as string,
      description: data.description as string,
      priority: data.priority as any,
      category: data.category as any,
      status: "open",
      created_by: { id: user.id, name: user.name, email: user.email, role: user.role },
      assigned_to: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    db.tickets.push(newTicket);
    return HttpResponse.json(newTicket, { status: 201 });
  }),

  http.patch(`${API_URL}/tickets/:id`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const ticketIndex = db.tickets.findIndex(t => t.id === parseInt(params.id as string));
    if (ticketIndex === -1) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });

    const ticket = db.tickets[ticketIndex];
    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }
    
    if (!canEditTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    const data = await request.json() as unknown as Record<string, unknown>;
    // Prevent unprivileged status changes
    if (user.role === 'customer' && data.status && data.status !== ticket.status) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    const updatedTicket = { ...ticket, ...data, updated_at: new Date().toISOString() };
    db.tickets[ticketIndex] = updatedTicket;

    return HttpResponse.json(updatedTicket);
  }),

  http.delete(`${API_URL}/tickets/:id`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const ticketIndex = db.tickets.findIndex(t => t.id === parseInt(params.id as string));
    if (ticketIndex === -1) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });

    const ticket = db.tickets[ticketIndex];
    
    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    if (!canDeleteTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    // Cascade delete comments
    db.comments = db.comments.filter(c => c.ticket_id !== ticket.id);
    db.tickets.splice(ticketIndex, 1);
    
    return new HttpResponse(null, { status: 204 });
  }),

  http.patch(`${API_URL}/tickets/:id/assign`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });
    
    const ticketIndex = db.tickets.findIndex(t => t.id === parseInt(params.id as string));
    if (ticketIndex === -1) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });
    const ticket = db.tickets[ticketIndex];

    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    const data = await request.json() as unknown as Record<string, unknown>;

    if (user.role === 'customer') {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    if (user.role === 'agent') {
      // Agent can only assign unassigned tickets to themselves
      if (ticket.assigned_to !== null) {
        return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
      }
      if (data.agent_id !== user.id) {
        return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
      }
    }

    if (user.role === 'admin') {
      // Admin can assign to active agents or themselves
      if (data.agent_id !== user.id) {
        const target = db.users.find(u => u.id === data.agent_id);
        if (!target || !target.is_active || target.role !== 'agent') {
          return HttpResponse.json({ detail: "Cannot assign to this user" }, { status: 403 });
        }
      }
    }

    const agent = db.users.find(u => u.id === data.agent_id);
    if (!agent) return HttpResponse.json({ detail: "Agent not found" }, { status: 404 });

    const updatedTicket = { 
      ...ticket, 
      assigned_to: { id: agent.id, name: agent.name, email: agent.email, role: agent.role },
      updated_at: new Date().toISOString() 
    };
    db.tickets[ticketIndex] = updatedTicket;

    return HttpResponse.json(updatedTicket);
  }),

  // ========================
  // COMMENTS ENDPOINTS
  // ========================

  http.get(`${API_URL}/tickets/:id/comments`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const ticketId = parseInt(params.id as string);
    const ticket = db.tickets.find(t => t.id === ticketId);
    
    if (!ticket) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });
    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    const comments = db.comments
      .filter(c => c.ticket_id === ticketId)
      .map(({ ticket_id, ...c }) => c); // Omit ticket_id in response

    return HttpResponse.json(comments);
  }),

  http.post(`${API_URL}/tickets/:id/comments`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const ticketId = parseInt(params.id as string);
    const ticket = db.tickets.find(t => t.id === ticketId);
    
    if (!ticket) return HttpResponse.json({ detail: "Ticket not found" }, { status: 404 });
    if (!canViewTicket(user, ticket)) {
      return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });
    }

    const data = await request.json() as unknown as Record<string, unknown>;
    
    const newComment: MockTicketComment = {
      id: db.comments.length > 0 ? Math.max(...db.comments.map(c => c.id)) + 1 : 1,
      content: data.content as string,
      author: { id: user.id, name: user.name, email: user.email, role: user.role },
      created_at: new Date().toISOString(),
      ticket_id: ticketId
    };
    
    db.comments.push(newComment);

    const { ticket_id, ...responseComment } = newComment;
    return HttpResponse.json(responseComment, { status: 201 });
  }),

  // ========================
  // DASHBOARD ENDPOINTS
  // ========================

  http.get(`${API_URL}/dashboard/summary`, async ({ request }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });

    const tickets = db.tickets.filter(t => canViewTicket(user, t));

    const summary: DashboardSummary = {
      total_tickets: tickets.length,
      open_tickets: tickets.filter(t => t.status === 'open').length,
      in_progress_tickets: tickets.filter(t => t.status === 'in_progress').length,
      waiting_customer_tickets: tickets.filter(t => t.status === 'waiting_customer').length,
      resolved_tickets: tickets.filter(t => t.status === 'resolved').length,
      closed_tickets: tickets.filter(t => t.status === 'closed').length,
      urgent_tickets: tickets.filter(t => t.priority === 'urgent').length,
      my_assigned_tickets: tickets.filter(t => t.assigned_to?.id === user.id).length,
    };

    return HttpResponse.json(summary);
  }),

  // ========================
  // USERS ENDPOINTS (Admin)
  // ========================

  http.get(`${API_URL}/users`, async ({ request }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });
    if (user.role !== 'admin') return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });

    const url = new URL(request.url);
    const page = parseInt(url.searchParams.get('page') || '1');
    const pageSize = parseInt(url.searchParams.get('page_size') || '10');
    const search = url.searchParams.get('search')?.toLowerCase();
    const role = url.searchParams.get('role');
    const isActive = url.searchParams.get('is_active');

    let users = db.users;

    if (search) users = users.filter(u => u.name.toLowerCase().includes(search) || u.email.toLowerCase().includes(search));
    if (role) users = users.filter(u => u.role === role);
    if (isActive) users = users.filter(u => String(u.is_active) === isActive);

    const total = users.length;
    const items = users.slice((page - 1) * pageSize, page * pageSize);

    return HttpResponse.json({
      items,
      page,
      page_size: pageSize,
      total,
      total_pages: Math.ceil(total / pageSize)
    });
  }),

  http.patch(`${API_URL}/users/:id`, async ({ request, params }) => {
    const user = getUserFromToken(request);
    if (!user) return HttpResponse.json({ detail: "Unauthorized" }, { status: 401 });
    if (user.role !== 'admin') return HttpResponse.json({ detail: "Forbidden" }, { status: 403 });

    const targetIndex = db.users.findIndex(u => u.id === parseInt(params.id as string));
    if (targetIndex === -1) return HttpResponse.json({ detail: "User not found" }, { status: 404 });

    const data = await request.json() as unknown as Record<string, unknown>;
    const updatedUser = { ...db.users[targetIndex], ...data };
    db.users[targetIndex] = updatedUser;

    return HttpResponse.json(updatedUser);
  })
];
