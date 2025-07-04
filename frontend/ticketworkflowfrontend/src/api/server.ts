import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;

export async function getTickets() {
  try {
    const response = await apiClient.get('tickets/');
    return response.data;
  } catch (error) {
    console.error('Błąd pobierania ticketów:', error);
    throw error;
  }
}