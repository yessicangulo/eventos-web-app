/**
 * Constantes de la aplicación
 */

// Roles de usuario
export const USER_ROLES = {
  ADMIN: 'admin',
  ORGANIZER: 'organizer',
  ATTENDEE: 'attendee',
};

// Estados de eventos
export const EVENT_STATUS = {
  SCHEDULED: 'scheduled',
  ONGOING: 'ongoing',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
};

// Etiquetas en español para los estados
export const EVENT_STATUS_LABELS = {
  [EVENT_STATUS.SCHEDULED]: 'Programado',
  [EVENT_STATUS.ONGOING]: 'En Curso',
  [EVENT_STATUS.COMPLETED]: 'Completado',
  [EVENT_STATUS.CANCELLED]: 'Cancelado',
};

// Etiquetas en español para los roles
export const USER_ROLE_LABELS = {
  [USER_ROLES.ADMIN]: 'Administrador',
  [USER_ROLES.ORGANIZER]: 'Organizador',
  [USER_ROLES.ATTENDEE]: 'Asistente',
};

// Configuración de paginación por defecto
export const DEFAULT_PAGE_SIZE = 6;
export const DEFAULT_PAGE = 1;
