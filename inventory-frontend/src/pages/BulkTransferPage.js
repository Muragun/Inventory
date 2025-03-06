import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const BulkTransferPage = () => {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [locations, setLocations] = useState([]);
  const [selectedItems, setSelectedItems] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Загружаем список предметов (например, с Dashboard) для выбора
  useEffect(() => {
    api.get('inventory-items/')
      .then(response => setItems(response.data))
      .catch(err => console.error('Ошибка получения предметов:', err));
  }, []);

  // Загружаем список локаций
  useEffect(() => {
    api.get('locations/')
      .then(response => setLocations(response.data))
      .catch(err => console.error('Ошибка получения локаций:', err));
  }, []);

  const handleCheckboxChange = (e, itemId) => {
    if (e.target.checked) {
      setSelectedItems(prev => [...prev, itemId]);
    } else {
      setSelectedItems(prev => prev.filter(id => id !== itemId));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedLocation) {
      setError('Выберите новую локацию.');
      return;
    }
    if (selectedItems.length === 0) {
      setError('Выберите хотя бы один предмет.');
      return;
    }
    setError('');
    // Отправляем запрос на массовый перенос
    api.post('inventory-items/bulk-transfer/', {
      item_ids: selectedItems,
      location_id: selectedLocation
    })
      .then(response => {
        setMessage('Предметы успешно перенесены.');
        // Можно перенаправить пользователя или обновить состояние
        setTimeout(() => navigate('/'), 2000);
      })
      .catch(err => {
        console.error('Ошибка массового переноса:', err);
        setError('Ошибка при переносе предметов.');
      });
  };

  return (
    <div>
      <h2>Массовый перенос предметов в новую локацию</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <h3>Выберите предметы:</h3>
          <ul>
            {items.map(item => (
              <li key={item.id}>
                <input
                  type="checkbox"
                  onChange={(e) => handleCheckboxChange(e, item.id)}
                />
                {item.name} (Инвентарный: {item.inventory_number || 'нет'}, Серийный: {item.serial_number || 'нет'})
              </li>
            ))}
          </ul>
        </div>
        <div>
          <label>Новая локация: </label>
          <select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            required
          >
            <option value="">Выберите локацию</option>
            {locations.map(loc => (
              <option key={loc.id} value={loc.id}>
                {loc.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Перенести выбранные предметы</button>
      </form>
    </div>
  );
};

export default BulkTransferPage;
