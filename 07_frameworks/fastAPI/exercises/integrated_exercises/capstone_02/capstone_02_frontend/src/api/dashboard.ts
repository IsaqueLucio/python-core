import { apiClient } from './client';
import type { DashboardSummary } from '../types/domain';

export const getDashboardSummary = async (): Promise<DashboardSummary> => {
  const response = await apiClient.get('/dashboard/summary');
  return response.data;
};
