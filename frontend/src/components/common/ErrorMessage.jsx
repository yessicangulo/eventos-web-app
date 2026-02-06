const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div style={{
      backgroundColor: '#fee',
      color: '#721c24',
      padding: '0.75rem 1rem',
      borderRadius: '8px',
      border: '1px solid #dc3545',
      marginBottom: '1rem',
      fontSize: '0.875rem',
    }}>
      {message}
    </div>
  );
};

export default ErrorMessage;
