import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Loading from '../common/Loading';

const PrivateRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return <Loading />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole) {
    const hasRole = user?.role === requiredRole || user?.role === 'admin';
    if (!hasRole) {
      return <Navigate to="/" replace />;
    }
  }

  return children;
};

export default PrivateRoute;
