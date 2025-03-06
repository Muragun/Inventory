import React, { useState, useEffect } from 'react';
import api from '../api';

const LocationReportPage = () => {
  const [report, setReport] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('reports/locations/full/')
      .then(response => {
        setReport(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Ошибка получения отчета по локациям:', err);
        setError('Ошибка получения отчета.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Загрузка отчета...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Полный отчет по локациям</h2>
      {report.map((loc, index) => (
        <div key={index} style={{ border: '1px solid #ccc', marginBottom: '1rem', padding: '1rem' }}>
          <h3>{loc.location}</h3>
          <p>{loc.description}</p>
          <p>Активных предметов: {loc.active_count}</p>
          <p>Снятых предметов: {loc.removed_count}</p>
          <h4>Активные предметы:</h4>
          <ul>
            {loc.active_items.map((item, i) => (
              <li key={i}>
                {item.name} (Серийный: {item.serial_number}, Назначен: {item.assigned_at})
              </li>
            ))}
          </ul>
          <h4>Снятые предметы:</h4>
          <ul>
            {loc.removed_items.map((item, i) => (
              <li key={i}>
                {item.name} (Серийный: {item.serial_number}, Назначен: {item.assigned_at}, Снято: {item.removed_at})
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default LocationReportPage;
