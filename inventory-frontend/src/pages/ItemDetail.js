import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

const ItemDetail = () => {
  const { id } = useParams();
  const [item, setItem] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    api.get(`inventory-items/${id}/`)
      .then(response => setItem(response.data))
      .catch(err => console.error('Ошибка получения предмета:', err));

    api.get(`inventory-items/${id}/history/`)
      .then(response => setHistory(response.data))
      .catch(err => console.error('Ошибка получения истории:', err));
  }, [id]);

  if (!item) return <div>Загрузка...</div>;

  return (
    <div>
      <h2>{item.name}</h2>
      <p>Серийный номер: {item.serial_number || 'нет'}</p>
      <p>Инвентарный номер: {item.inventory_number || 'нет'}</p>
      <p>Тип: {item.item_type_name || 'нет'}</p>
      <p>Текущая локация: {item.current_location || 'нет'}</p>
      
      <Link to={`/edit-item/${id}`}>Редактировать предмет</Link> |{' '}
      <Link to={`/transfer-item/${id}`}>Переместить предмет</Link>
      
      <h3>История перемещений</h3>
      <ul>
        {history.map((entry, index) => (
          <li key={index}>
            Локация: {entry.location_name} – Дата назначения: {entry.assigned_at}
            {entry.removed_at && `, Снято: ${entry.removed_at}`}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ItemDetail;
