import { apiClient } from './client';
import type { TicketComment } from '../types/domain';

export const getTicketComments = async (ticketId: number): Promise<TicketComment[]> => {
  const response = await apiClient.get(`/tickets/${ticketId}/comments`);
  return response.data;
};

export const createTicketComment = async (ticketId: number, content: string): Promise<TicketComment> => {
  const response = await apiClient.post(`/tickets/${ticketId}/comments`, { content });
  return response.data;
};
