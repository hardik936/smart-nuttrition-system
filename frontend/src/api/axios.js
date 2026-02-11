import axios from 'axios';

const configuredApiUrl = import.meta.env.VITE_API_URL;

const api = axios.create({
    baseURL: configuredApiUrl || 'http://localhost:8000',
});

if (!configuredApiUrl && typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    console.warn('VITE_API_URL is not configured. API calls may fail in deployed frontend.');
}

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
