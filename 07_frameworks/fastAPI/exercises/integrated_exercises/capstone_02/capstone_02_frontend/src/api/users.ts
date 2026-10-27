import { apiClient } from './client';
import type { User, PaginatedResponse } from '../types/domain';

export interface GetUsersParams {
  page?: number;
  page_size?: number;
  search?: string;
  role?: string;
  is_active?: boolean;
}

export const getUsers = async (params?: GetUsersParams): Promise<PaginatedResponse<User>> => {
  const response = await apiClient.get('/users', { params });
  return response.data;
};

export const updateUser = async (id: number, data: Partial<User>): Promise<User> => {
  const response = await apiClient.patch(`/users/${id}`, data);
  return response.data;
};
