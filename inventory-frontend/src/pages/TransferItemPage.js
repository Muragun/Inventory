import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

const TransferItemPage = () => {
  const { id } = useParams(); // ID предмета для переноса
  const navigate = useNavigate();
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState('');
  const [error, setError] = useState('');

  // Загружаем список локаций при монтировании компонента
  useEffect(() => {
    api.get('locations/')
      .then(response => {
        setLocations(response.data);
      })
      .catch(err => {
        console.error('Ошибка получения локаций:', err);
        setError('Ошибка получения локаций.');
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedLocation) {
      setError('Пожалуйста, выберите локацию.');
      return;
    }
    // POST-запрос для переноса предмета
    api.post(`inventory-items/${id}/transfer/`, { location_id: selectedLocation })
      .then(response => {
        // После переноса перенаправляем на страницу деталей предмета
        navigate(`/item/${id}`);
      })
      .catch(err => {
        console.error('Ошибка переноса предмета:', err);
        setError('Ошибка переноса предмета.');
      });
  };

  return (
    <div>
      <h2>Перенос предмета в новую локацию</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Перенести предмет</button>
      </form>
    </div>
  );
};

export default TransferItemPage;
