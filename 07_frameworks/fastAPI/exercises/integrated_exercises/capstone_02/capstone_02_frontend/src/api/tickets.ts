import { apiClient } from './client';
import type { Ticket, PaginatedResponse } from '../types/domain';

export interface GetTicketsParams {
  page?: number;
  page_size?: number;
  status?: string;
  priority?: string;
  category?: string;
  search?: string;
  assigned_to_me?: boolean;
}

export const getTickets = async (params?: GetTicketsParams): Promise<PaginatedResponse<Ticket>> => {
  const response = await apiClient.get('/tickets', { params });
  return response.data;
};

export const getTicket = async (id: number): Promise<Ticket> => {
  const response = await apiClient.get(`/tickets/${id}`);
  return response.data;
};

export const createTicket = async (data: Partial<Ticket>): Promise<Ticket> => {
  const response = await apiClient.post('/tickets', data);
  return response.data;
};

export const updateTicket = async (id: number, data: Partial<Ticket>): Promise<Ticket> => {
  const response = await apiClient.patch(`/tickets/${id}`, data);
  return response.data;
};

export const deleteTicket = async (id: number): Promise<void> => {
  await apiClient.delete(`/tickets/${id}`);
};

export const assignTicket = async (id: number, agentId: number): Promise<Ticket> => {
  const response = await apiClient.patch(`/tickets/${id}/assign`, { agent_id: agentId });
  return response.data;
};
