import { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

/**
 * Contexto de autenticación
 * Maneja el estado global de autenticación del usuario
 */
const AuthContext = createContext(null);

/**
 * Hook para usar el contexto de autenticación
 * @returns {Object} Contexto de autenticación con user, loading, login, register, logout
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

/**
 * Proveedor del contexto de autenticación
 * @param {Object} props - Props del componente
 * @param {React.ReactNode} props.children - Componentes hijos
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Verificar autenticación al cargar la app
   * Si hay un token en localStorage, intenta obtener el usuario actual
   */
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (err) {
        // Si el token es inválido o expiró, limpiar localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  /**
   * Iniciar sesión
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @returns {Promise<void>}
   */
  const login = async (email, password) => {
    try {
      setError(null);
      setLoading(true);

      // Llamar al servicio de login
      const tokenData = await authService.login(email, password);

      // Guardar token en localStorage
      localStorage.setItem('token', tokenData.access_token);

      // Obtener datos del usuario actual
      const userData = await authService.getCurrentUser();
      setUser(userData);

      // Guardar usuario en localStorage (opcional, para persistencia)
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Error al iniciar sesión';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Registrar nuevo usuario
   * @param {string} email - Email del usuario
   * @param {string} password - Contraseña del usuario
   * @param {string} [fullName] - Nombre completo (opcional)
   * @returns {Promise<void>}
   */
  const register = async (email, password, fullName = null) => {
    try {
      setError(null);
      setLoading(true);

      // Registrar usuario
      const userData = await authService.register(email, password, fullName);

      // Después del registro, hacer login automático
      // El backend no retorna token en registro, así que hacemos login
      const tokenData = await authService.login(email, password);

      // Guardar token en localStorage
      localStorage.setItem('token', tokenData.access_token);

      // Obtener datos completos del usuario (con eventos registrados)
      const fullUserData = await authService.getCurrentUser();
      setUser(fullUserData);

      // Guardar usuario en localStorage
      localStorage.setItem('user', JSON.stringify(fullUserData));
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al registrar usuario';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cerrar sesión
   * Limpia el token y el usuario del estado y localStorage
   */
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setError(null);
  };

  /**
   * Actualizar datos del usuario
   * Útil cuando se actualiza el perfil o se realizan acciones que cambian el estado del usuario
   * @returns {Promise<void>}
   */
  const refreshUser = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
    } catch (err) {
      // Si falla, hacer logout
      logout();
      throw err;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    refreshUser,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
