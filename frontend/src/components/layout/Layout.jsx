import Navbar from './Navbar';

const Layout = ({ children }) => {
  const containerStyle = {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
  };

  const contentStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem',
  };

  return (
    <div style={containerStyle}>
      <Navbar />
      <main style={contentStyle}>{children}</main>
    </div>
  );
};

export default Layout;
