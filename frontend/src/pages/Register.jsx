import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/layout/Layout';
import Card from '../components/common/Card';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorMessage from '../components/common/ErrorMessage';
import Loading from '../components/common/Loading';

const Register = () => {
  const navigate = useNavigate();
  const { register, loading: authLoading } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: null,
      }));
    }
    if (error) {
      setError(null);
    }
  };

  const validate = () => {
    const newErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'El email no es válido';
    }

    if (!formData.password) {
      newErrors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 6) {
      newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Por favor confirma tu contraseña';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Las contraseñas no coinciden';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await register(
        formData.email,
        formData.password,
        formData.fullName.trim() || null
      );
      navigate('/');
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail || err.message || 'Error al registrar usuario';
      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  };

  const headerStyle = {
    textAlign: 'center',
    marginBottom: '2rem',
  };

  const titleStyle = {
    fontSize: '2rem',
    fontWeight: 'bold',
    marginBottom: '0.5rem',
    color: '#333',
  };

  const subtitleStyle = {
    color: '#666',
    fontSize: '1rem',
  };

  const linkStyle = {
    color: '#646cff',
    textDecoration: 'none',
  };

  const footerStyle = {
    textAlign: 'center',
    marginTop: '1.5rem',
    color: '#666',
  };

  const isLoading = isSubmitting || authLoading;

  if (authLoading && !isSubmitting) {
    return (
      <Layout>
        <Loading />
      </Layout>
    );
  }

  return (
    <Layout>
      <div style={{ maxWidth: '450px', margin: '0 auto' }}>
        <Card>
          <div style={headerStyle}>
            <h1 style={titleStyle}>Crear Cuenta</h1>
            <p style={subtitleStyle}>Regístrate para comenzar a usar la plataforma</p>
          </div>

          {error && <ErrorMessage message={error} />}

          <form onSubmit={handleSubmit} style={formStyle}>
            <Input
              label="Nombre Completo (Opcional)"
              name="fullName"
              type="text"
              value={formData.fullName}
              onChange={handleChange}
              error={errors.fullName}
              placeholder="Juan Pérez"
            />

            <Input
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              placeholder="tu@email.com"
              required
            />

            <Input
              label="Contraseña"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              placeholder="••••••••"
              required
            />

            <Input
              label="Confirmar Contraseña"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              error={errors.confirmPassword}
              placeholder="••••••••"
              required
            />

            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Registrando...' : 'Registrarse'}
            </Button>
          </form>

          <div style={footerStyle}>
            <p>
              ¿Ya tienes una cuenta?{' '}
              <Link to="/login" style={linkStyle}>
                Inicia sesión aquí
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </Layout>
  );
};

export default Register;
