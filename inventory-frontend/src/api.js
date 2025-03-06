import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/'; // Адрес нашего backend API

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Интерсептор добавляет JWT-токен (если он сохранен в localStorage)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
