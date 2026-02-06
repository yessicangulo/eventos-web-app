import api from './api';

/**
 * Servicio de sesiones
 * Maneja todas las operaciones relacionadas con sesiones de eventos
 */
export const sessionService = {
  /**
   * Obtener sesiones de un evento con paginación
   * @param {number} eventId - ID del evento
   * @param {Object} [params] - Parámetros de paginación
   * @param {number} [params.page=1] - Número de página
   * @param {number} [params.per_page=20] - Resultados por página
   * @returns {Promise<{
   *   sessions: Array,
   *   pagination: {
   *     page: number,
   *     per_page: number,
   *     total: number,
   *     total_pages: number
   *   }
   * }>}
   */
  getByEvent: async (eventId, params = {}) => {
    const queryParams = new URLSearchParams();

    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page) queryParams.append('per_page', params.per_page.toString());

    const queryString = queryParams.toString();
    const url = `/sessions/event/${eventId}${queryString ? `?${queryString}` : ''}`;

    const response = await api.get(url);
    return response.data;
  },

  /**
   * Obtener detalle de una sesión por ID
   * @param {number} id - ID de la sesión
   * @returns {Promise<{
   *   id: number,
   *   event_id: number,
   *   title: string,
   *   description: string | null,
   *   speaker_name: string | null,
   *   speaker_bio: string | null,
   *   start_time: string,
   *   end_time: string,
   *   location: string | null,
   *   capacity: number | null,
   *   created_at: string
   * }>}
   */
  getById: async (id) => {
    const response = await api.get(`/sessions/${id}`);
    return response.data;
  },

  /**
   * Crear nueva sesión
   * Requiere rol ORGANIZER
   * @param {Object} data - Datos de la sesión
   * @param {number} data.event_id - ID del evento
   * @param {string} data.title - Título de la sesión
   * @param {string} [data.description] - Descripción de la sesión
   * @param {string} [data.speaker_name] - Nombre del ponente
   * @param {string} [data.speaker_bio] - Biografía del ponente
   * @param {string} data.start_time - Hora de inicio (ISO 8601)
   * @param {string} data.end_time - Hora de fin (ISO 8601)
   * @param {string} [data.location] - Ubicación de la sesión
   * @param {number} [data.capacity] - Capacidad máxima
   * @returns {Promise<{
   *   id: number,
   *   event_id: number,
   *   title: string,
   *   description: string | null,
   *   speaker_name: string | null,
   *   speaker_bio: string | null,
   *   start_time: string,
   *   end_time: string,
   *   location: string | null,
   *   capacity: number | null,
   *   created_at: string
   * }>}
   */
  create: async (data) => {
    const response = await api.post('/sessions', data);
    return response.data;
  },

  /**
   * Actualizar sesión existente
   * Requiere rol ORGANIZER
   * @param {number} id - ID de la sesión
   * @param {Object} data - Datos a actualizar (todos los campos son opcionales)
   * @param {string} [data.title] - Título de la sesión
   * @param {string} [data.description] - Descripción de la sesión
   * @param {string} [data.speaker_name] - Nombre del ponente
   * @param {string} [data.speaker_bio] - Biografía del ponente
   * @param {string} [data.start_time] - Hora de inicio (ISO 8601)
   * @param {string} [data.end_time] - Hora de fin (ISO 8601)
   * @param {string} [data.location] - Ubicación de la sesión
   * @param {number} [data.capacity] - Capacidad máxima
   * @returns {Promise<{
   *   id: number,
   *   event_id: number,
   *   title: string,
   *   description: string | null,
   *   speaker_name: string | null,
   *   speaker_bio: string | null,
   *   start_time: string,
   *   end_time: string,
   *   location: string | null,
   *   capacity: number | null,
   *   created_at: string
   * }>}
   */
  update: async (id, data) => {
    const response = await api.put(`/sessions/${id}`, data);
    return response.data;
  },

  /**
   * Eliminar sesión
   * Requiere rol ORGANIZER
   * @param {number} id - ID de la sesión
   * @returns {Promise<void>}
   */
  delete: async (id) => {
    await api.delete(`/sessions/${id}`);
  },
};
