import EventCard from './EventCard';
import Loading from '../common/Loading';
import ErrorMessage from '../common/ErrorMessage';

const EventList = ({ events, pagination, loading, error, onPageChange }) => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '2rem',
  };

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '1.5rem',
  };

  const paginationStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '1rem',
    marginTop: '2rem',
  };

  const buttonStyle = {
    padding: '0.6rem 1.2rem',
    backgroundColor: '#646cff',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '0.95rem',
    fontWeight: 500,
    transition: 'background-color 0.2s ease',
  };

  const disabledButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
  };

  const pageInfoStyle = {
    fontSize: '0.95rem',
    color: '#666',
  };

  const emptyStateStyle = {
    textAlign: 'center',
    padding: '3rem',
    color: '#666',
  };

  if (loading) {
    return <Loading />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (!events || events.length === 0) {
    return (
      <div style={emptyStateStyle}>
        <p style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>No se encontraron eventos</p>
        <p>Intenta ajustar los filtros de búsqueda</p>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <div style={gridStyle}>
        {events.map((event) => (
          <EventCard key={event.id} event={event} />
        ))}
      </div>

      {pagination && pagination.total_pages > 1 && (
        <div style={paginationStyle}>
          <button
            style={pagination.page === 1 ? disabledButtonStyle : buttonStyle}
            onClick={() => onPageChange && onPageChange(pagination.page - 1)}
            disabled={pagination.page === 1}
            onMouseEnter={(e) => {
              if (pagination.page !== 1) {
                e.target.style.backgroundColor = '#535bf2';
              }
            }}
            onMouseLeave={(e) => {
              if (pagination.page !== 1) {
                e.target.style.backgroundColor = '#646cff';
              }
            }}
          >
            Anterior
          </button>

          <span style={pageInfoStyle}>
            Página {pagination.page} de {pagination.total_pages} ({pagination.total} eventos)
          </span>

          <button
            style={pagination.page === pagination.total_pages ? disabledButtonStyle : buttonStyle}
            onClick={() => onPageChange && onPageChange(pagination.page + 1)}
            disabled={pagination.page === pagination.total_pages}
            onMouseEnter={(e) => {
              if (pagination.page !== pagination.total_pages) {
                e.target.style.backgroundColor = '#535bf2';
              }
            }}
            onMouseLeave={(e) => {
              if (pagination.page !== pagination.total_pages) {
                e.target.style.backgroundColor = '#646cff';
              }
            }}
          >
            Siguiente
          </button>
        </div>
      )}
    </div>
  );
};

export default EventList;
