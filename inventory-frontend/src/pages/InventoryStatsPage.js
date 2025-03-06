import React, { useState, useEffect } from 'react';
import api from '../api';

const InventoryStatsPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('reports/stats/')
      .then(response => {
        setStats(response.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Ошибка получения статистики:', err);
        setError('Ошибка получения статистики.');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Загрузка статистики...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <h2>Статистика инвентаря</h2>
      <p>Общее количество предметов: {stats.total_items}</p>
      <p>Активных предметов: {stats.active_items}</p>
      <h3>Статистика по типам:</h3>
      <ul>
        {stats.items_by_type.map((type, index) => (
          <li key={index}>
            {type.item_type__name}: {type.count} предметов, общая стоимость: {type.total_cost}
          </li>
        ))}
      </ul>
      <h3>Статистика по локациям:</h3>
      <ul>
        {stats.items_by_location.map((loc, index) => (
          <li key={index}>
            {loc.name}: {loc.active_items_count} активных назначений
          </li>
        ))}
      </ul>
    </div>
  );
};

export default InventoryStatsPage;
