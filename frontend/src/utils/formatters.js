/**
 * Funciones simples para formatear fechas
 *
 * El backend envía fechas como "2024-03-15T14:30:00"
 * Estas funciones las convierten a formato legible en español
 */

/**
 * Convierte una fecha a formato legible
 * Ejemplo: "2024-03-15" → "15 de marzo de 2024"
 */
export const formatDate = (date) => {
  if (!date) return '';

  const fecha = new Date(date);

  // Si la fecha es inválida, devolver cadena vacía
  if (isNaN(fecha.getTime())) {
    return '';
  }

  return fecha.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Convierte una fecha y hora a formato legible
 * Ejemplo: "2024-03-15T14:30:00" → "15 de marzo de 2024, 14:30"
 */
export const formatDateTime = (date) => {
  if (!date) return '';

  const fecha = new Date(date);

  // Si la fecha es inválida, devolver cadena vacía
  if (isNaN(fecha.getTime())) {
    return '';
  }

  return fecha.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};
