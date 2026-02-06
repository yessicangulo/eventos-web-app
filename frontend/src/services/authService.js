import api from './api';

/**
 * Servicio de autenticación
 * Maneja login, registro y obtención del perfil del usuario actual
 */
export const authService = {
  /**
   * Iniciar sesión
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @returns {Promise<{access_token: string, token_type: string}>}
   */
  login: async (email, password) => {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  /**
   * Registrar nuevo usuario
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @param {string} [fullName] - Nombre completo (opcional)
   * @returns {Promise<{
   *   id: number,
   *   email: string,
   *   full_name: string | null,
   *   role: string,
   *   is_active: boolean,
   *   created_at: string
   * }>}
   */
  register: async (email, password, fullName = null) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  /**
   * Obtener perfil del usuario actual
   * @returns {Promise<{
   *   id: number,
   *   email: string,
   *   full_name: string | null,
   *   role: string,
   *   is_active: boolean,
   *   created_at: string,
   *   registered_events: Array,
   *   created_events_count: number
   * }>}
   */
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};
