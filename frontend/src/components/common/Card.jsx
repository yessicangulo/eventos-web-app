import React from 'react';

const Card = ({ children }) => {
  return (
    <div style={{
      backgroundColor: '#ffffff',
      borderRadius: '6px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      padding: '1.5rem',
    }}>
      {children}
    </div>
  );
};

export default Card;
