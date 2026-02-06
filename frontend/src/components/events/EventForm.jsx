import { useState, useEffect } from 'react';
import Card from '../common/Card';
import Input from '../common/Input';
import Button from '../common/Button';
import ErrorMessage from '../common/ErrorMessage';
import { EVENT_STATUS } from '../../utils/constants';

const EventForm = ({
  event,
  onSubmit,
  onCancel,
  loading: externalLoading,
  error: externalError,
}) => {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    location: '',
    start_date: '',
    end_date: '',
    capacity: '',
    status: EVENT_STATUS.SCHEDULED,
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (event) {
      const formatDateForInput = dateString => {
        if (!dateString) return '';
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}`;
      };

      setFormData({
        name: event.name || '',
        description: event.description || '',
        location: event.location || '',
        start_date: formatDateForInput(event.start_date),
        end_date: formatDateForInput(event.end_date),
        capacity: event.capacity?.toString() || '',
        status: event.status || EVENT_STATUS.SCHEDULED,
      });
    }
  }, [event]);

  // Determinar qué campos son editables según el estado del evento
  const getEditableFields = () => {
    if (!event) {
      // Crear nuevo evento: todos los campos son editables
      return {
        name: true,
        description: true,
        location: true,
        start_date: true,
        end_date: true,
        capacity: true,
        status: false, // No se puede cambiar estado al crear
      };
    }

    const computedStatus = event.computed_status || EVENT_STATUS.SCHEDULED;
    const now = new Date();
    const startDate = new Date(event.start_date);

    // Reglas de negocio según el estado
    switch (computedStatus) {
      case EVENT_STATUS.SCHEDULED:
        // SCHEDULED: name, description, location, capacity, status editables
        // Fechas solo si el evento NO ha iniciado
        const canEditDates = now < startDate;
        return {
          name: true,
          description: true,
          location: true,
          start_date: canEditDates,
          end_date: canEditDates,
          capacity: true,
          status: true,
        };

      case EVENT_STATUS.ONGOING:
        // ONGOING: Solo description y location
        return {
          name: false,
          description: true,
          location: true,
          start_date: false,
          end_date: false,
          capacity: false,
          status: false,
        };

      case EVENT_STATUS.COMPLETED:
        // COMPLETED: Nada es editable
        return {
          name: false,
          description: false,
          location: false,
          start_date: false,
          end_date: false,
          capacity: false,
          status: false,
        };

      case EVENT_STATUS.CANCELLED:
        // CANCELLED: Solo status (para reactivar)
        return {
          name: false,
          description: false,
          location: false,
          start_date: false,
          end_date: false,
          capacity: false,
          status: true, // Solo para reactivar a SCHEDULED
        };

      default:
        return {
          name: true,
          description: true,
          location: true,
          start_date: true,
          end_date: true,
          capacity: true,
          status: true,
        };
    }
  };

  const editableFields = getEditableFields();

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null,
      }));
    }
  };

  const validate = () => {
    const newErrors = {};

    // Solo validar campos que son editables
    if (editableFields.name && !formData.name.trim()) {
      newErrors.name = 'El nombre del evento es requerido';
    }

    if (editableFields.start_date && !formData.start_date) {
      newErrors.start_date = 'La fecha de inicio es requerida';
    }

    if (editableFields.end_date && !formData.end_date) {
      newErrors.end_date = 'La fecha de fin es requerida';
    }

    if (
      editableFields.start_date &&
      editableFields.end_date &&
      formData.start_date &&
      formData.end_date
    ) {
      const start = new Date(formData.start_date);
      const end = new Date(formData.end_date);
      if (end <= start) {
        newErrors.end_date = 'La fecha de fin debe ser posterior a la fecha de inicio';
      }
    }

    if (editableFields.capacity && (!formData.capacity || parseInt(formData.capacity) <= 0)) {
      newErrors.capacity = 'La capacidad debe ser mayor a 0';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async e => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Solo incluir campos editables en el submit
      const submitData = {};

      if (editableFields.name) {
        submitData.name = formData.name.trim();
      }
      if (editableFields.description) {
        submitData.description = formData.description.trim() || null;
      }
      if (editableFields.location) {
        submitData.location = formData.location.trim() || null;
      }
      if (editableFields.start_date) {
        submitData.start_date = new Date(formData.start_date).toISOString();
      }
      if (editableFields.end_date) {
        submitData.end_date = new Date(formData.end_date).toISOString();
      }
      if (editableFields.capacity) {
        submitData.capacity = parseInt(formData.capacity);
      }
      if (editableFields.status && event && formData.status !== event.status) {
        submitData.status = formData.status;
      }

      await onSubmit(submitData);
    } catch (err) {
      console.error('Error al enviar formulario:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  };

  const buttonGroupStyle = {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'flex-end',
    marginTop: '1rem',
  };

  const isModeEdit = !!event;
  const isLoading = isSubmitting || externalLoading;

  // Verificar si hay al menos un campo editable
  const hasEditableFields = Object.values(editableFields).some(value => value === true);

  // Si el evento está completado, no se puede editar nada
  const isCompleted = event?.computed_status === EVENT_STATUS.COMPLETED;

  return (
    <Card>
      <h2 style={{ marginTop: 0, marginBottom: '1.5rem' }}>
        {isModeEdit ? 'Editar Evento' : 'Crear Nuevo Evento'}
      </h2>

      {externalError && <ErrorMessage message={externalError} />}

      {isCompleted && <ErrorMessage message="Este evento está completado y no se puede editar." />}

      <form onSubmit={handleSubmit} style={formStyle}>
        {/* Mensaje informativo según el estado */}
        {event && (
          <div
            style={{
              padding: '1rem',
              backgroundColor: '#e3f2fd',
              borderRadius: '8px',
              marginBottom: '1rem',
              fontSize: '0.9rem',
              color: '#1976d2',
            }}
          >
            <strong>Estado del evento:</strong>{' '}
            {event.computed_status === EVENT_STATUS.SCHEDULED && 'Programado'}
            {event.computed_status === EVENT_STATUS.ONGOING && 'En Curso'}
            {event.computed_status === EVENT_STATUS.COMPLETED && 'Completado'}
            {event.computed_status === EVENT_STATUS.CANCELLED && 'Cancelado'}
            {event.computed_status === EVENT_STATUS.ONGOING &&
              ' - Solo puedes editar descripción y ubicación'}
            {event.computed_status === EVENT_STATUS.COMPLETED &&
              ' - Este evento no se puede editar'}
            {event.computed_status === EVENT_STATUS.CANCELLED &&
              ' - Solo puedes reactivar el evento cambiando el estado'}
          </div>
        )}

        <Input
          label="Nombre del Evento *"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          error={errors.name}
          required={!event}
          disabled={!editableFields.name}
        />

        <Input
          label="Descripción"
          name="description"
          type="textarea"
          value={formData.description}
          onChange={handleChange}
          error={errors.description}
          disabled={!editableFields.description}
        />

        <Input
          label="Ubicación"
          name="location"
          type="text"
          value={formData.location}
          onChange={handleChange}
          error={errors.location}
          disabled={!editableFields.location}
        />

        <Input
          label="Fecha y Hora de Inicio *"
          name="start_date"
          type="datetime-local"
          value={formData.start_date}
          onChange={handleChange}
          error={errors.start_date}
          required={!event}
          disabled={!editableFields.start_date}
        />

        <Input
          label="Fecha y Hora de Fin *"
          name="end_date"
          type="datetime-local"
          value={formData.end_date}
          onChange={handleChange}
          error={errors.end_date}
          required={!event}
          disabled={!editableFields.end_date}
        />

        <Input
          label="Capacidad Máxima *"
          name="capacity"
          type="number"
          value={formData.capacity}
          onChange={handleChange}
          error={errors.capacity}
          min="1"
          required={!event}
          disabled={!editableFields.capacity}
        />

        {isModeEdit && editableFields.status && (
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
              Estado
            </label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              disabled={!editableFields.status}
              style={{
                width: '100%',
                padding: '0.6rem',
                borderRadius: '8px',
                border: '1px solid #ddd',
                fontSize: '1rem',
                backgroundColor: editableFields.status ? '#fff' : '#f5f5f5',
                cursor: editableFields.status ? 'pointer' : 'not-allowed',
                opacity: editableFields.status ? 1 : 0.6,
              }}
            >
              <option value={EVENT_STATUS.SCHEDULED}>Programado</option>
              <option value={EVENT_STATUS.CANCELLED}>Cancelado</option>
            </select>
            <p style={{ fontSize: '0.85rem', color: '#666', marginTop: '0.25rem' }}>
              {event?.computed_status === EVENT_STATUS.CANCELLED
                ? 'Puedes reactivar el evento cambiando el estado a "Programado" (solo si el evento no ha iniciado)'
                : 'Los estados "En Curso" y "Completado" se calculan automáticamente según las fechas'}
            </p>
          </div>
        )}

        <div style={buttonGroupStyle}>
          {onCancel && (
            <Button
              type="button"
              onClick={onCancel}
              disabled={isLoading}
              style={{ backgroundColor: '#666' }}
            >
              Cancelar
            </Button>
          )}
          <Button type="submit" disabled={isLoading || !hasEditableFields || isCompleted}>
            {isLoading ? 'Guardando...' : isModeEdit ? 'Actualizar Evento' : 'Crear Evento'}
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default EventForm;
