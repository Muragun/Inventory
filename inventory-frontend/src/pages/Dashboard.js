import React, { useState, useEffect } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get('inventory-items/').then(response => {
      setItems(response.data);
    }).catch(err => {
      console.error('Ошибка получения данных:', err);
    });
  }, []);

  return (
    <div>
      <h2>Список инвентарных предметов</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <Link to={`/item/${item.id}`}>
              {item.name} ({item.serial_number || 'без номера'})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
