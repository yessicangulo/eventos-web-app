const Input = ({ label, error, type = 'text', disabled = false, ...props }) => {
  const inputStyle = {
    width: '100%',
    padding: '0.6rem 0.8rem',
    border: error ? '1px solid #dc3545' : '1px solid #ccc',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
    transition: 'border-color 0.2s ease',
    fontFamily: 'inherit',
    backgroundColor: disabled ? '#f5f5f5' : '#fff',
    cursor: disabled ? 'not-allowed' : 'text',
    opacity: disabled ? 0.6 : 1,
  };

  const isTextarea = type === 'textarea';

  return (
    <div style={{ marginBottom: '1rem' }}>
      {label && (
        <label style={{
          display: 'block',
          marginBottom: '0.5rem',
          fontSize: '0.875rem',
          fontWeight: 500,
        }}>
          {label}
        </label>
      )}
      {isTextarea ? (
        <textarea
          style={{
            ...inputStyle,
            minHeight: '100px',
            resize: disabled ? 'none' : 'vertical',
          }}
          disabled={disabled}
          onFocus={(e) => {
            if (!disabled) {
              e.target.style.borderColor = error ? '#dc3545' : '#646cff';
            }
          }}
          onBlur={(e) => {
            if (!disabled) {
              e.target.style.borderColor = error ? '#dc3545' : '#ccc';
            }
          }}
          {...props}
        />
      ) : (
        <input
          type={type}
          style={inputStyle}
          disabled={disabled}
          onFocus={(e) => {
            if (!disabled) {
              e.target.style.borderColor = error ? '#dc3545' : '#646cff';
            }
          }}
          onBlur={(e) => {
            if (!disabled) {
              e.target.style.borderColor = error ? '#dc3545' : '#ccc';
            }
          }}
          {...props}
        />
      )}
      {error && (
        <div style={{
          color: '#dc3545',
          fontSize: '0.875rem',
          marginTop: '0.25rem'
        }}>
          {error}
        </div>
      )}
    </div>
  );
};

export default Input;
