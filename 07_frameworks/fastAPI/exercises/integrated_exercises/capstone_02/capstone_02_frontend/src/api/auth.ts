import { apiClient } from './client';
import type { User } from '../types/domain';

export const login = async (username: string, password: string):Promise<{access_token: string, token_type: string}> => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  
  const response = await apiClient.post('/auth/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  return response.data;
};

export const register = async (data: Record<string, unknown>): Promise<User> => {
  const response = await apiClient.post('/auth/register', data);
  return response.data;
};

export const getMe = async (): Promise<User> => {
  const response = await apiClient.get('/auth/me');
  return response.data;
};
