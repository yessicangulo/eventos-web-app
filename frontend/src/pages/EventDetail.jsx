import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventService } from '../services/eventService';
import { attendeeService } from '../services/attendeeService';
import Layout from '../components/layout/Layout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import { formatDateTime } from '../utils/formatters';
import { EVENT_STATUS_LABELS } from '../utils/constants';

const headerStyle = {
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'flex-start',
  marginBottom: '1.5rem',
};

const EventDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, refreshUser } = useAuth();

  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isRegistered, setIsRegistered] = useState(false);
  const [checkingRegistration, setCheckingRegistration] = useState(false);
  const [registering, setRegistering] = useState(false);
  const [registerError, setRegisterError] = useState(null);

  useEffect(() => {
    fetchEvent();
  }, [id]);

  useEffect(() => {
    if (user && user.role === 'attendee' && event) {
      checkRegistration();
    }
  }, [user, event]);

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

  const checkRegistration = async () => {
    if (!user || user.role !== 'attendee') return;

    setCheckingRegistration(true);
    try {
      const response = await attendeeService.checkRegistration(parseInt(id));
      setIsRegistered(response.is_registered || false);
    } catch (err) {
      console.error('Error al verificar registro:', err);
    } finally {
      setCheckingRegistration(false);
    }
  };

  const handleRegister = async () => {
    if (!user) {
      navigate('/login');
      return;
    }

    setRegistering(true);
    setRegisterError(null);

    try {
      if (isRegistered) {
        await attendeeService.unregister(parseInt(id));
        setIsRegistered(false);
      } else {
        await attendeeService.register(parseInt(id));
        setIsRegistered(true);
      }
      await refreshUser();
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al procesar el registro';
      setRegisterError(errorMessage);
    } finally {
      setRegistering(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('¿Estás seguro de que deseas eliminar este evento?')) {
      return;
    }

    try {
      await eventService.delete(id);
      navigate('/');
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al eliminar el evento';
      alert(errorMessage);
    }
  };

  const canEdit = user &&
                event &&
                (user.role === 'organizer' || user.role === 'admin') &&
                event.computed_status !== 'completed';
  const canDelete = canEdit;
  const canRegister = user && user.role === 'attendee' && event && !event.is_full;

  if (loading) {
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
        <Button onClick={() => navigate('/')}>Volver a Inicio</Button>
      </Layout>
    );
  }

  if (!event) {
    return (
      <Layout>
        <ErrorMessage message="Evento no encontrado" />
        <Button onClick={() => navigate('/')}>Volver a Inicio</Button>
      </Layout>
    );
  }

  const statusBadgeStyle = {
    padding: '0.5rem 1rem',
    borderRadius: '12px',
    fontSize: '0.9rem',
    fontWeight: 500,
    display: 'inline-block',
    marginBottom: '1rem',
  };

  const getStatusBadgeColor = (status) => {
    const colors = {
      scheduled: { backgroundColor: '#e3f2fd', color: '#1976d2' },
      ongoing: { backgroundColor: '#fff3e0', color: '#f57c00' },
      completed: { backgroundColor: '#e8f5e9', color: '#388e3c' },
      cancelled: { backgroundColor: '#ffebee', color: '#d32f2f' },
    };
    return colors[status] || { backgroundColor: '#f5f5f5', color: '#666' };
  };

  const infoSectionStyle = {
    marginBottom: '1.5rem',
  };

  const infoRowStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    marginBottom: '0.75rem',
    fontSize: '1rem',
  };

  const sessionsSectionStyle = {
    marginTop: '1rem',
  };

  const sessionCardStyle = {
    backgroundColor: '#f9f9f9',
    padding: '1rem',
    borderRadius: '8px',
    marginBottom: '1rem',
  };

  const buttonGroupStyle = {
    display: 'flex',
    gap: '1rem',
    marginTop: '1.5rem',
    flexWrap: 'wrap',
  };

  return (
    <Layout>
      <div style={{ maxWidth: '900px', margin: '0 auto' }}>
        <Button
          onClick={() => navigate('/')}
          style={{ marginBottom: '1.5rem', backgroundColor: '#666' }}
        >
          ← Volver
        </Button>

        <Card>
          <div style={headerStyle}>
            <div>
              <h1 style={{ marginTop: 0, marginBottom: '0.5rem', fontSize: '2rem' }}>
                {event.name}
              </h1>
              <span
                style={{
                  ...statusBadgeStyle,
                  ...getStatusBadgeColor(event.computed_status),
                }}
              >
                {EVENT_STATUS_LABELS[event.computed_status] || event.computed_status}
              </span>
            </div>
          </div>

          {event.description && (
            <div style={infoSectionStyle}>
              <p style={{ fontSize: '1.1rem', lineHeight: '1.6', color: '#555' }}>
                {event.description}
              </p>
            </div>
          )}

          <div style={infoSectionStyle}>
            {event.location && (
              <div style={infoRowStyle}>
                <strong>📍 Ubicación:</strong> {event.location}
              </div>
            )}
            <div style={infoRowStyle}>
              <strong>📅 Fecha de Inicio:</strong> {formatDateTime(event.start_date)}
            </div>
            <div style={infoRowStyle}>
              <strong>📅 Fecha de Fin:</strong> {formatDateTime(event.end_date)}
            </div>
            <div style={infoRowStyle}>
              <strong>👥 Capacidad:</strong>{' '}
              {event.is_full ? (
                <span style={{ color: '#d32f2f', fontWeight: 'bold' }}>
                  Lleno ({event.capacity} / {event.capacity})
                </span>
              ) : (
                <span style={{ color: '#388e3c' }}>
                  {event.available_capacity} de {event.capacity} disponibles
                </span>
              )}
            </div>
          </div>

          {registerError && <ErrorMessage message={registerError} />}

          <div style={buttonGroupStyle}>
            {canRegister && (
              <Button
                onClick={handleRegister}
                disabled={registering || checkingRegistration}
              >
                {registering
                  ? 'Procesando...'
                  : isRegistered
                  ? 'Cancelar Registro'
                  : 'Registrarse al Evento'}
              </Button>
            )}

            {canEdit && (
              <Button
                onClick={() => navigate(`/events/${id}/edit`)}
                style={{ backgroundColor: '#388e3c' }}
              >
                Editar Evento
              </Button>
            )}

            {canDelete && (
              <Button
                onClick={handleDelete}
                style={{ backgroundColor: '#d32f2f' }}
              >
                Eliminar Evento
              </Button>
            )}

            {!user && (
              <Button onClick={() => navigate('/login')}>
                Inicia sesión para registrarte
              </Button>
            )}
          </div>


        </Card>

        {event.sessions && event.sessions.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
          <Card>
            <div style={sessionsSectionStyle}>
              <h2 style={{ marginTop: 0, marginBottom: '1.5rem' }}>Sesiones del Evento</h2>
              {event.sessions.map((session) => (
                <div key={session.id} style={sessionCardStyle}>
                  <h3 style={{ marginTop: 0, marginBottom: '0.5rem' }}>{session.title}</h3>
                  {session.description && (
                    <p style={{ color: '#666', marginBottom: '0.5rem' }}>
                      {session.description}
                    </p>
                  )}
                  {session.speaker_name && (
                    <p style={{ marginBottom: '0.5rem' }}>
                      <strong>Ponente:</strong> {session.speaker_name}
                    </p>
                  )}
                  <p style={{ marginBottom: '0.5rem', fontSize: '0.9rem', color: '#555' }}>
                    <strong>Horario:</strong> {formatDateTime(session.start_time)} -{' '}
                    {formatDateTime(session.end_time)}
                  </p>
                  {session.location && (
                    <p style={{ marginBottom: 0, fontSize: '0.9rem', color: '#555' }}>
                      <strong>Ubicación:</strong> {session.location}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </Card>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default EventDetail;
