import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <nav style={{ padding: '1rem', backgroundColor: '#eee' }}>
      <Link to="/">Dashboard</Link> |{' '}
      <Link to="/create-item">Добавить предмет</Link> |{' '}
      <Link to="/bulk-transfer">Массовый перенос</Link> |{' '}
      <Link to="/import-csv">Импорт CSV</Link> |{' '}
      <Link to="/reports/location">Отчет по локациям</Link> |{' '}
      <Link to="/reports/stats">Статистика</Link> |{' '}
      <button onClick={handleLogout}>Выйти</button>
    </nav>
  );
};

export default Navbar;
