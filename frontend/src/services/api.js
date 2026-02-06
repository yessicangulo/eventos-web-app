import axios from 'axios';

// Base URL del backend FastAPI
// Intentar usar 127.0.0.1 primero (más compatible), luego localhost
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api/v1';

// Crear instancia de Axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir token automáticamente a todas las peticiones
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

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Manejar errores 401 (no autorizado) - limpiar token
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // Nota: La redirección a login se manejará en los componentes/páginas
    }

    // Mejorar mensajes de error de red
    if (!error.response) {
      // Error de red (backend no disponible, CORS, etc.)
      if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
        console.error('Network Error Details:', {
          code: error.code,
          message: error.message,
          config: error.config,
          url: error.config?.url,
        });
        error.message = 'No se pudo conectar con el servidor. Verifica que el backend esté corriendo y que CORS esté configurado correctamente. Backend esperado en: http://127.0.0.1:5000';
      }
    } else if (error.response?.status === 0) {
      // Error CORS típico
      error.message = 'Error de CORS: El backend no permite peticiones desde este origen. Verifica BACKEND_CORS_ORIGINS en el backend.';
    }

    return Promise.reject(error);
  }
);

export default api;
