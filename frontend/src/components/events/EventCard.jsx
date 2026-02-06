import { Link } from 'react-router-dom';
import Card from '../common/Card';
import { formatDateTime } from '../../utils/formatters';
import { EVENT_STATUS_LABELS } from '../../utils/constants';

const EventCard = ({ event }) => {
  const cardContentStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  };

  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '1rem',
  };

  const titleStyle = {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    margin: 0,
    color: '#333',
    textDecoration: 'none',
  };

  const statusBadgeStyle = {
    padding: '0.25rem 0.75rem',
    borderRadius: '12px',
    fontSize: '0.85rem',
    fontWeight: 500,
    whiteSpace: 'nowrap',
  };

  const getStatusBadgeColor = status => {
    const colors = {
      scheduled: { backgroundColor: '#e3f2fd', color: '#1976d2' },
      ongoing: { backgroundColor: '#fff3e0', color: '#f57c00' },
      completed: { backgroundColor: '#e8f5e9', color: '#388e3c' },
      cancelled: { backgroundColor: '#ffebee', color: '#d32f2f' },
    };
    return colors[status] || { backgroundColor: '#f5f5f5', color: '#666' };
  };

  const descriptionStyle = {
    color: '#666',
    fontSize: '0.95rem',
    lineHeight: '1.5',
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden',
  };

  const infoStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    fontSize: '0.9rem',
    color: '#555',
  };

  const infoRowStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  };

  const capacityStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    marginTop: '0.5rem',
  };

  const capacityTextStyle = {
    fontSize: '0.9rem',
    color: event.is_full ? '#d32f2f' : '#388e3c',
    fontWeight: 500,
  };

  const linkStyle = {
    textDecoration: 'none',
    color: 'inherit',
  };

  return (
    <Card>
      <div style={cardContentStyle}>
        <div style={headerStyle}>
          <Link to={`/events/${event.id}`} style={linkStyle}>
            <h3 style={titleStyle}>{event.name}</h3>
          </Link>
          <span
            style={{
              ...statusBadgeStyle,
              ...getStatusBadgeColor(event.computed_status),
            }}
          >
            {EVENT_STATUS_LABELS[event.computed_status] || event.computed_status}
          </span>
        </div>

        {event.description && <p style={descriptionStyle}>{event.description}</p>}

        <div style={infoStyle}>
          {event.location && (
            <div style={infoRowStyle}>
              <strong>📍 Ubicación:</strong> {event.location}
            </div>
          )}
          <div style={infoRowStyle}>
            <strong>📅 Inicio:</strong> {formatDateTime(event.start_date)}
          </div>
          <div style={infoRowStyle}>
            <strong>📅 Fin:</strong> {formatDateTime(event.end_date)}
          </div>
        </div>

        <div style={capacityStyle}>
          <span style={capacityTextStyle}>
            {event.is_full
              ? '🔴 Lleno'
              : `✅ ${event.available_capacity} de ${event.capacity} disponibles`}
          </span>
        </div>

        <Link to={`/events/${event.id}`} style={linkStyle}>
          <button
            style={{
              padding: '0.6rem 1.2rem',
              backgroundColor: '#646cff',
              color: '#ffffff',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.95rem',
              fontWeight: 500,
              width: '100%',
              marginTop: '0.5rem',
              transition: 'background-color 0.2s ease',
            }}
            onMouseEnter={e => (e.target.style.backgroundColor = '#535bf2')}
            onMouseLeave={e => (e.target.style.backgroundColor = '#646cff')}
          >
            Ver Detalles
          </button>
        </Link>
      </div>
    </Card>
  );
};

export default EventCard;
