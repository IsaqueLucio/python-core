import axios from 'axios';

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    // Timeout error
    if (error.code === 'ECONNABORTED') {
      return 'The request timed out. Please try again.';
    }

    // Network error (no response)
    if (!error.response) {
      return 'A network error occurred. Please check your connection.';
    }

    // FastAPI 422: detail is usually an array of validation errors
    if (error.response.status === 422) {
      const detail = error.response.data?.detail;
      if (Array.isArray(detail)) {
        return detail.map((err: Record<string, unknown>) => {
          const loc = err.loc as string[] | undefined;
          const field = loc?.[loc.length - 1] || 'Field';
          return `${field}: ${err.msg}`;
        }).join(' | ');
      }
    }

    // Standard FastAPI error detail string
    const detail = error.response.data?.detail;
    if (detail && typeof detail === 'string') {
      return detail;
    }

    // Fallback messages by status
    switch (error.response.status) {
      case 400: return 'Bad request. Please check the submitted data.';
      case 401: return 'Session expired or unauthorized. Please log in again.';
      case 403: return 'You do not have permission to perform this action.';
      case 404: return 'The requested resource was not found.';
      case 409: return 'Conflict: The resource already exists.';
      case 500: return 'Internal server error. Please try again later.';
      default: return `An unexpected error occurred (Status: ${error.response.status}).`;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An unknown error occurred.';
}
