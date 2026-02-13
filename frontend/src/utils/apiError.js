import axios from 'axios';

export const isApiBaseUrlMissingInProd = () => {
  // Always return false to allow axios fallback URL to work
  return false;
};

export const getFriendlyApiError = (err, fallbackMessage = 'Request failed') => {
  if (isApiBaseUrlMissingInProd()) {
    return 'Deployment config issue: VITE_API_URL is not set. Add your backend URL in frontend environment variables and redeploy.';
  }

  if (axios.isAxiosError(err)) {
    if (!err.response) {
      return 'Cannot reach backend API. Check VITE_API_URL and backend service status.';
    }

    const detail = err.response?.data?.detail;
    if (typeof detail === 'string' && detail.trim()) {
      return detail;
    }

    if (Array.isArray(detail)) {
      const first = detail[0];
      if (first?.msg) return first.msg;
      return JSON.stringify(detail);
    }

    if (err.response.status >= 500) {
      return 'Server error from backend. Please check backend logs and DATABASE_URL configuration.';
    }

    if (err.response.status === 404) {
      return 'API route not found. Verify VITE_API_URL points to backend service.';
    }

    return fallbackMessage;
  }

  return fallbackMessage;
};
