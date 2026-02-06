import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { USER_ROLES, USER_ROLE_LABELS } from '../../utils/constants';
import Button from '../common/Button';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navStyle = {
    backgroundColor: '#ffffff',
    borderBottom: '1px solid #e0e0e0',
    padding: '1rem 2rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
  };

  const logoStyle = {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#646cff',
    textDecoration: 'none',
    marginRight: '2rem',
  };

  const linksStyle = {
    display: 'flex',
    gap: '1.5rem',
    alignItems: 'center',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  };

  const linkStyle = {
    color: '#333',
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: 500,
    transition: 'color 0.2s ease',
  };

  const userInfoStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  };

  const userEmailStyle = {
    color: '#666',
    fontSize: '0.9rem',
  };

  return (
    <nav style={navStyle}>
      <Link to="/" style={logoStyle}>
        Eventos
      </Link>

      <ul style={linksStyle}>
        <li>
          <Link
            to="/"
            style={linkStyle}
            onMouseEnter={e => (e.target.style.color = '#646cff')}
            onMouseLeave={e => (e.target.style.color = '#333')}
          >
            Inicio
          </Link>
        </li>

        {isAuthenticated ? (
          <>
            <li>
              <Link
                to="/profile"
                style={linkStyle}
                onMouseEnter={e => (e.target.style.color = '#646cff')}
                onMouseLeave={e => (e.target.style.color = '#333')}
              >
                Mi Perfil
              </Link>
            </li>
            <li style={userInfoStyle}>
              <span style={userEmailStyle}>
                {user?.email} ({USER_ROLE_LABELS[user?.role] || 'Usuario'})
              </span>
              <Button
                onClick={handleLogout}
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}
              >
                Cerrar Sesión
              </Button>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link
                to="/login"
                style={linkStyle}
                onMouseEnter={e => (e.target.style.color = '#646cff')}
                onMouseLeave={e => (e.target.style.color = '#333')}
              >
                Iniciar Sesión
              </Link>
            </li>
            <li>
              <Link
                to="/register"
                style={linkStyle}
                onMouseEnter={e => (e.target.style.color = '#646cff')}
                onMouseLeave={e => (e.target.style.color = '#333')}
              >
                Registrarse
              </Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
