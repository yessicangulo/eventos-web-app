import api from './api';

/**
 * Servicio de asistentes
 * Maneja todas las operaciones relacionadas con el registro de asistentes a eventos
 */
export const attendeeService = {
  /**
   * Registrarse a un evento
   * Requiere rol ATTENDEE
   * @param {number} eventId - ID del evento
   * @returns {Promise<{message: string, data: {event_id: number, registered_at: string}}>}
   */
  register: async (eventId) => {
    const response = await api.post(`/attendees/register/${eventId}`);
    return response.data;
  },

  /**
   * Cancelar registro a un evento
   * Requiere rol ATTENDEE
   * @param {number} eventId - ID del evento
   * @returns {Promise<void>}
   */
  unregister: async (eventId) => {
    await api.delete(`/attendees/unregister/${eventId}`);
  },

  /**
   * Obtener eventos a los que el usuario actual está registrado
   * Requiere rol ATTENDEE
   * @param {Object} [params] - Parámetros de paginación
   * @param {number} [params.page=1] - Número de página
   * @param {number} [params.per_page=20] - Resultados por página
   * @returns {Promise<{
   *   events: Array,
   *   pagination: {
   *     page: number,
   *     per_page: number,
   *     total: number,
   *     total_pages: number
   *   }
   * }>}
   */
  getMyEvents: async (params = {}) => {
    const queryParams = new URLSearchParams();

    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page) queryParams.append('per_page', params.per_page.toString());

    const queryString = queryParams.toString();
    const url = `/attendees/my-events${queryString ? `?${queryString}` : ''}`;

    const response = await api.get(url);
    return response.data;
  },

  /**
   * Verificar si el usuario actual está registrado en un evento
   * Requiere rol ATTENDEE
   * @param {number} eventId - ID del evento
   * @returns {Promise<{is_registered: boolean}>}
   */
  checkRegistration: async (eventId) => {
    const response = await api.get(`/attendees/check/${eventId}`);
    return response.data;
  },
};
