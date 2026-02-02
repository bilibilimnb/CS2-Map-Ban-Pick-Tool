import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;

// 房间相关 API
export const roomApi = {
  getByCode: (roomCode: string) => api.get(`/rooms/${roomCode}`),
  join: (roomId: string, data: any) => api.post(`/rooms/${roomId}/join`, data),
  updateReady: (roomId: string, data: any) => api.post(`/rooms/${roomId}/ready`, data),
  getUsers: (roomId: string) => api.get(`/rooms/${roomId}/users`),
  startBP: (roomId: string) => api.post(`/rooms/${roomId}/bp/start`),
  getBPStatus: (roomId: string) => api.get(`/rooms/${roomId}/bp/status`),
};

// 管理员相关 API
export const adminApi = {
  login: (data: { username: string; password: string }) => api.post('/admin/login', data),
  createMapPool: (data: any) => api.post('/admin/mappools', data),
  getMapPools: () => api.get('/admin/mappools'),
  createRoom: (data: any) => api.post('/admin/rooms', data),
  getRooms: (params?: any) => api.get('/admin/rooms', { params }),
  getRoomDetail: (roomId: string) => api.get(`/admin/rooms/${roomId}`),
  getBPRecord: (roomId: string) => api.get(`/admin/rooms/${roomId}/bp-record`),
};
