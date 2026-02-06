import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventService } from '../services/eventService';
import Layout from '../components/layout/Layout';
import EventForm from '../components/events/EventForm';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import { USER_ROLES } from '../utils/constants';

const EditEvent = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();

  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [saveError, setSaveError] = useState(null);

  useEffect(() => {
    fetchEvent();
  }, [id]);

  const fetchEvent = async () => {
    setLoading(true);
    setError(null);

    try {
      const eventData = await eventService.getById(id);
      setEvent(eventData);
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al cargar el evento';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data) => {
    setSaving(true);
    setSaveError(null);

    try {
      const updatedEvent = await eventService.update(id, data);
      navigate(`/events/${updatedEvent.id}`);
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al actualizar el evento';
      setSaveError(errorMessage);
      throw err;
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    navigate(`/events/${id}`);
  };

  if (authLoading || loading) {
    return (
      <Layout>
        <Loading />
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <ErrorMessage message={error} />
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '0.6rem 1.2rem',
            backgroundColor: '#646cff',
            color: '#ffffff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            marginTop: '1rem',
          }}
        >
          Volver a Inicio
        </button>
      </Layout>
    );
  }

  if (!user) {
    return (
      <Layout>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Debes iniciar sesión para editar eventos</p>
          <button
            onClick={() => navigate('/login')}
            style={{
              padding: '0.6rem 1.2rem',
              backgroundColor: '#646cff',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              marginTop: '1rem',
            }}
          >
            Ir a Login
          </button>
        </div>
      </Layout>
    );
  }

  if (!event) {
    return (
      <Layout>
        <ErrorMessage message="Evento no encontrado" />
        <button
          onClick={() => navigate('/')}
          style={{
            padding: '0.6rem 1.2rem',
            backgroundColor: '#646cff',
            color: '#ffffff',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            marginTop: '1rem',
          }}
        >
          Volver a Inicio
        </button>
      </Layout>
    );
  }

  const canEdit = (user.role === USER_ROLES.ORGANIZER || user.role === USER_ROLES.ADMIN);

  if (!canEdit) {
    return (
      <Layout>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>No tienes permisos para editar este evento.</p>
          <button
            onClick={() => navigate(`/events/${id}`)}
            style={{
              padding: '0.6rem 1.2rem',
              backgroundColor: '#646cff',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              marginTop: '1rem',
            }}
          >
            Volver al Evento
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <EventForm
          event={event}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          loading={saving}
          error={saveError}
        />
      </div>
    </Layout>
  );
};

export default EditEvent;
