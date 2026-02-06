import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventService } from '../services/eventService';
import Layout from '../components/layout/Layout';
import EventList from '../components/events/EventList';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import Loading from '../components/common/Loading';
import { DEFAULT_PAGE_SIZE, DEFAULT_PAGE, EVENT_STATUS } from '../utils/constants';

const Home = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();

  const [events, setEvents] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [filters, setFilters] = useState({
    page: DEFAULT_PAGE,
    per_page: DEFAULT_PAGE_SIZE,
    search: '',
    status: '',
  });

  const fetchEvents = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = {
        page: filters.page,
        per_page: filters.per_page,
      };

      if (filters.search.trim()) {
        params.search = filters.search.trim();
      }

      if (filters.status) {
        params.status = filters.status;
      }

      const response = await eventService.getAll(params);
      setEvents(response.events || []);
      setPagination(response.pagination || null);
    } catch (err) {
      // Manejar errores de red de forma más amigable
      if (err.code === 'ERR_NETWORK' || err.message === 'Network Error') {
        setError('No se pudo conectar con el servidor. Verifica que el backend esté corriendo en http://localhost:5000');
      } else {
        const errorMessage =
          err.response?.data?.detail || err.message || 'Error al cargar eventos';
        setError(errorMessage);
      }
    } finally {
      setLoading(false);
    }
  };

  // Solo cargar eventos si el usuario está autenticado
  useEffect(() => {
    if (!authLoading && user) {
      fetchEvents();
    }
  }, [filters.page, filters.status, user, authLoading]);

  const handlePageChange = (newPage) => {
    setFilters((prev) => ({
      ...prev,
      page: newPage,
    }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setFilters((prev) => ({
      ...prev,
      page: DEFAULT_PAGE,
    }));
    fetchEvents();
  };

  const handleSearchChange = (e) => {
    setFilters((prev) => ({
      ...prev,
      search: e.target.value,
    }));
  };

  const handleStatusChange = (e) => {
    setFilters((prev) => ({
      ...prev,
      status: e.target.value,
      page: DEFAULT_PAGE,
    }));
  };

  const canCreateEvent = user && (user.role === 'organizer' || user.role === 'admin');

  // Si está cargando la autenticación, mostrar loading
  if (authLoading) {
    return (
      <Layout>
        <Loading />
      </Layout>
    );
  }

  // Si no está autenticado, mostrar página de bienvenida
  if (!user) {
    const welcomeStyle = {
      textAlign: 'center',
      padding: '3rem 1rem',
      maxWidth: '600px',
      margin: '0 auto',
    };

    const titleStyle = {
      fontSize: '2.5rem',
      fontWeight: 'bold',
      marginBottom: '1rem',
      color: '#333',
    };

    const subtitleStyle = {
      fontSize: '1.2rem',
      color: '#666',
      marginBottom: '2.5rem',
      lineHeight: '1.6',
    };

    const buttonGroupStyle = {
      display: 'flex',
      gap: '1rem',
      justifyContent: 'center',
      flexWrap: 'wrap',
    };

    return (
      <Layout>
        <Card>
          <div style={welcomeStyle}>
            <h1 style={titleStyle}>Bienvenido a Mis Eventos</h1>
            <p style={subtitleStyle}>
              Plataforma para gestionar y descubrir eventos increíbles.
              Inicia sesión o regístrate para comenzar.
            </p>
            <div style={buttonGroupStyle}>
              <Button onClick={() => navigate('/login')} style={{ minWidth: '150px' }}>
                Iniciar Sesión
              </Button>
              <Button
                onClick={() => navigate('/register')}
                style={{
                  minWidth: '150px',
                  backgroundColor: '#388e3c'
                }}
              >
                Registrarse
              </Button>
            </div>
          </div>
        </Card>
      </Layout>
    );
  }

  // Si está autenticado, mostrar eventos
  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
    flexWrap: 'wrap',
    gap: '1rem',
  };

  const titleStyle = {
    fontSize: '2rem',
    fontWeight: 'bold',
    margin: 0,
    color: '#333',
  };

  const filtersStyle = {
    display: 'flex',
    gap: '1rem',
    marginBottom: '0',
    flexWrap: 'wrap',
    alignItems: 'flex-end',
  };

  const searchFormStyle = {
    display: 'flex',
    gap: '0.5rem',
    flex: '1',
    minWidth: '250px',
  };

  const selectStyle = {
    padding: '0.6rem',
    borderRadius: '8px',
    border: '1px solid #ccc',
    fontSize: '1rem',
    minWidth: '150px',
  };

  const eventListContainerStyle = {
    marginTop: '2rem',
  };

  return (
    <Layout>
      <div style={headerStyle}>
        <h1 style={titleStyle}>Eventos Disponibles</h1>
        {canCreateEvent && (
          <Button onClick={() => navigate('/events/create')}>
            + Crear Evento
          </Button>
        )}
      </div>

      <Card>
        <form onSubmit={handleSearch} style={filtersStyle}>
          <div style={searchFormStyle}>
            <input
              type="text"
              placeholder="Buscar eventos..."
              value={filters.search}
              onChange={handleSearchChange}
              style={{
                flex: '1',
                padding: '0.6rem 0.6rem',
                border: '1px solid #ccc',
                borderRadius: '6px',
                fontSize: '1rem',
                outline: 'none',
              }}
            />
            <Button type="submit">Buscar</Button>
          </div>

          <select
            value={filters.status}
            onChange={handleStatusChange}
            style={selectStyle}
          >
            <option value="">Todos los estados</option>
            <option value={EVENT_STATUS.SCHEDULED}>Programado</option>
            <option value={EVENT_STATUS.ONGOING}>En Curso</option>
            <option value={EVENT_STATUS.COMPLETED}>Completado</option>
            <option value={EVENT_STATUS.CANCELLED}>Cancelado</option>
          </select>
        </form>
      </Card>

      <div style={eventListContainerStyle}>
        <EventList
          events={events}
          pagination={pagination}
          loading={loading}
          error={error}
          onPageChange={handlePageChange}
        />
      </div>
    </Layout>
  );
};

export default Home;
