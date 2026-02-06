const Button = ({ children, onClick, disabled = false, ...props }) => {
  const buttonStyle = {
    padding: '0.6rem 1.2rem',
    backgroundColor: disabled ? '#ccc' : '#646cff',
    color: '#ffffff',
    border: 'none',
    borderRadius: '8px',
    cursor: disabled ? 'not-allowed' : 'pointer',
    fontSize: '1rem',
    fontWeight: 500,
    transition: 'background-color 0.2s ease', // Solo esto
  };

  return (
    <button
      style={buttonStyle}
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={e => {
        if (!disabled) e.target.style.backgroundColor = '#535bf2';
      }}
      onMouseLeave={e => {
        if (!disabled) e.target.style.backgroundColor = '#646cff';
      }}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
