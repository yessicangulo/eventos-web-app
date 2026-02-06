import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventService } from '../services/eventService';
import { attendeeService } from '../services/attendeeService';
import Layout from '../components/layout/Layout';
import Card from '../components/common/Card';
import EventList from '../components/events/EventList';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import Button from '../components/common/Button';
import { DEFAULT_PAGE_SIZE, DEFAULT_PAGE, USER_ROLE_LABELS } from '../utils/constants';

const Profile = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading, logout } = useAuth();

  const [createdEvents, setCreatedEvents] = useState([]);
  const [registeredEvents, setRegisteredEvents] = useState([]);
  const [createdPagination, setCreatedPagination] = useState(null);
  const [registeredPagination, setRegisteredPagination] = useState(null);
  const [loadingCreated, setLoadingCreated] = useState(false);
  const [loadingRegistered, setLoadingRegistered] = useState(false);
  const [errorCreated, setErrorCreated] = useState(null);
  const [errorRegistered, setErrorRegistered] = useState(null);

  const [createdPage, setCreatedPage] = useState(DEFAULT_PAGE);
  const [registeredPage, setRegisteredPage] = useState(DEFAULT_PAGE);

  useEffect(() => {
    if (user) {
      if (user.role === 'organizer' || user.role === 'admin') {
        fetchCreatedEvents();
      }
      if (user.role === 'attendee') {
        fetchRegisteredEvents();
      }
    }
  }, [user, createdPage, registeredPage]);

  const fetchCreatedEvents = async () => {
    setLoadingCreated(true);
    setErrorCreated(null);

    try {
      const response = await eventService.getMyEvents({
        page: createdPage,
        per_page: DEFAULT_PAGE_SIZE,
      });
      setCreatedEvents(response.events || []);
      setCreatedPagination(response.pagination || null);
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al cargar eventos creados';
      setErrorCreated(errorMessage);
    } finally {
      setLoadingCreated(false);
    }
  };

  const fetchRegisteredEvents = async () => {
    setLoadingRegistered(true);
    setErrorRegistered(null);

    try {
      const response = await attendeeService.getMyEvents({
        page: registeredPage,
        per_page: DEFAULT_PAGE_SIZE,
      });
      setRegisteredEvents(response.events || []);
      setRegisteredPagination(response.pagination || null);
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al cargar eventos registrados';
      setErrorRegistered(errorMessage);
    } finally {
      setLoadingRegistered(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (authLoading) {
    return (
      <Layout>
        <Loading />
      </Layout>
    );
  }

  if (!user) {
    return (
      <Layout>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>Debes iniciar sesión para ver tu perfil</p>
          <Button onClick={() => navigate('/login')}>Ir a Login</Button>
        </div>
      </Layout>
    );
  }

  const isOrganizer = user.role === 'organizer' || user.role === 'admin';
  const isAttendee = user.role === 'attendee';

  const profileHeaderStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '2rem',
    flexWrap: 'wrap',
    gap: '1rem',
  };

  const userInfoStyle = {
    flex: '1',
  };

  const titleStyle = {
    fontSize: '2rem',
    fontWeight: 'bold',
    marginTop: 0,
    marginBottom: '0.5rem',
    color: '#333',
  };

  const infoRowStyle = {
    marginBottom: '0.5rem',
    fontSize: '1rem',
    color: '#666',
  };

  const sectionStyle = {
    marginTop: '3rem',
  };

  const sectionTitleStyle = {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    marginBottom: '1.5rem',
    color: '#333',
  };

  return (
    <Layout>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <Card>
          <div style={profileHeaderStyle}>
            <div style={userInfoStyle}>
              <h1 style={titleStyle}>Mi Perfil</h1>
              <div style={infoRowStyle}>
                <strong>Email:</strong> {user.email}
              </div>
              {user.full_name && (
                <div style={infoRowStyle}>
                  <strong>Nombre:</strong> {user.full_name}
                </div>
              )}
              <div style={infoRowStyle}>
                <strong>Rol:</strong> {USER_ROLE_LABELS[user.role] || user.role}
              </div>
              {isOrganizer && (
                <div style={infoRowStyle}>
                  <strong>Eventos creados:</strong> {user.created_events_count || 0}
                </div>
              )}
            </div>
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {isOrganizer && (
                <Button onClick={() => navigate('/events/create')}>+ Crear Evento</Button>
              )}
              <Button onClick={handleLogout} style={{ backgroundColor: '#d32f2f' }}>
                Cerrar Sesión
              </Button>
            </div>
          </div>
        </Card>

        {isOrganizer && (
          <div style={sectionStyle}>
            <h2 style={sectionTitleStyle}>Mis Eventos Creados</h2>
            <EventList
              events={createdEvents}
              pagination={createdPagination}
              loading={loadingCreated}
              error={errorCreated}
              onPageChange={setCreatedPage}
            />
          </div>
        )}

        {isAttendee && (
          <div style={sectionStyle}>
            <h2 style={sectionTitleStyle}>Eventos en los que estoy Registrado</h2>
            <EventList
              events={registeredEvents}
              pagination={registeredPagination}
              loading={loadingRegistered}
              error={errorRegistered}
              onPageChange={setRegisteredPage}
            />
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Profile;
