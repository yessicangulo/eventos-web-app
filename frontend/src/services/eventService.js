import api from './api';

/**
 * Servicio de eventos
 * Maneja todas las operaciones relacionadas con eventos
 */
export const eventService = {
  /**
   * Obtener lista de eventos con paginación y filtros
   * @param {Object} [params] - Parámetros de búsqueda y paginación
   * @param {number} [params.page=1] - Número de página
   * @param {number} [params.per_page=20] - Resultados por página
   * @param {string} [params.search] - Búsqueda por nombre
   * @param {string} [params.status] - Filtrar por estado (scheduled, ongoing, completed, cancelled)
   * @returns {Promise<{events: Array, pagination: {page: number, per_page: number, total: number, total_pages: number}}>}
   */
  getAll: async (params = {}) => {
    const queryParams = new URLSearchParams();

    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page) queryParams.append('per_page', params.per_page.toString());
    if (params.search) queryParams.append('search', params.search);
    if (params.status) queryParams.append('status', params.status);

    const queryString = queryParams.toString();
    const url = `/events${queryString ? `?${queryString}` : ''}`;

    const response = await api.get(url);
    return response.data;
  },

  /**
   * Obtener detalle de un evento por ID
   * @param {number} id - ID del evento
   * @returns {Promise<{
   *   id: number,
   *   name: string,
   *   description: string | null,
   *   location: string | null,
   *   start_date: string,
   *   end_date: string,
   *   capacity: number,
   *   computed_status: string,
   *   creator_id: number,
   *   created_at: string,
   *   available_capacity: number,
   *   is_full: boolean,
   *   sessions: Array
   * }>}
   */
  getById: async id => {
    const response = await api.get(`/events/${id}`);
    return response.data;
  },

  /**
   * Crear nuevo evento
   * Requiere rol ORGANIZER
   * @param {Object} data - Datos del evento
   * @param {string} data.name - Nombre del evento
   * @param {string} [data.description] - Descripción del evento
   * @param {string} [data.location] - Ubicación del evento
   * @param {string} data.start_date - Fecha de inicio (ISO 8601)
   * @param {string} data.end_date - Fecha de fin (ISO 8601)
   * @param {number} data.capacity - Capacidad máxima
   * @returns {Promise<{
   *   id: number,
   *   name: string,
   *   description: string | null,
   *   location: string | null,
   *   start_date: string,
   *   end_date: string,
   *   capacity: number,
   *   computed_status: string,
   *   creator_id: number,
   *   created_at: string,
   *   available_capacity: number,
   *   is_full: boolean
   * }>}
   */
  create: async data => {
    const response = await api.post('/events', data);
    return response.data;
  },

  /**
   * Actualizar evento existente
   * Requiere rol ORGANIZER
   * @param {number} id - ID del evento
   * @param {Object} data - Datos a actualizar (todos los campos son opcionales)
   * @param {string} [data.name] - Nombre del evento
   * @param {string} [data.description] - Descripción del evento
   * @param {string} [data.location] - Ubicación del evento
   * @param {string} [data.start_date] - Fecha de inicio (ISO 8601)
   * @param {string} [data.end_date] - Fecha de fin (ISO 8601)
   * @param {number} [data.capacity] - Capacidad máxima
   * @param {string} [data.status] - Estado (scheduled o cancelled)
   * @returns {Promise<{
   *   id: number,
   *   name: string,
   *   description: string | null,
   *   location: string | null,
   *   start_date: string,
   *   end_date: string,
   *   capacity: number,
   *   computed_status: string,
   *   creator_id: number,
   *   created_at: string,
   *   available_capacity: number,
   *   is_full: boolean
   * }>}
   */
  update: async (id, data) => {
    const response = await api.put(`/events/${id}`, data);
    return response.data;
  },

  /**
   * Eliminar evento
   * Requiere rol ORGANIZER
   * @param {number} id - ID del evento
   * @returns {Promise<void>}
   */
  delete: async id => {
    await api.delete(`/events/${id}`);
  },

  /**
   * Obtener eventos creados por el usuario actual
   * Requiere rol ORGANIZER o ADMIN
   * @param {Object} [params] - Parámetros de paginación
   * @param {number} [params.page=1] - Número de página
   * @param {number} [params.per_page=20] - Resultados por página
   * @returns {Promise<{events: Array, pagination: {page: number, per_page: number, total: number, total_pages: number}}>}
   */
  getMyEvents: async (params = {}) => {
    const queryParams = new URLSearchParams();

    if (params.page) queryParams.append('page', params.page.toString());
    if (params.per_page) queryParams.append('per_page', params.per_page.toString());

    const queryString = queryParams.toString();
    const url = `/events/my/events${queryString ? `?${queryString}` : ''}`;

    const response = await api.get(url);
    return response.data;
  },
};
