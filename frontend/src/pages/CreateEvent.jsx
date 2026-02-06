import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { eventService } from '../services/eventService';
import Layout from '../components/layout/Layout';
import EventForm from '../components/events/EventForm';
import Loading from '../components/common/Loading';
import { USER_ROLES } from '../utils/constants';

const CreateEvent = () => {
  const navigate = useNavigate();
  const { user, loading: authLoading } = useAuth();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async data => {
    setLoading(true);
    setError(null);

    try {
      const newEvent = await eventService.create(data);
      navigate(`/events/${newEvent.id}`);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error al crear el evento';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
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
          <p>Debes iniciar sesión para crear eventos</p>
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

  if (user.role !== USER_ROLES.ORGANIZER && user.role !== USER_ROLES.ADMIN) {
    return (
      <Layout>
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <p>No tienes permisos para crear eventos. Se requiere rol de Organizador.</p>
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
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <EventForm
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          loading={loading}
          error={error}
        />
      </div>
    </Layout>
  );
};

export default CreateEvent;
