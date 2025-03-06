import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api';

const EditItemPage = () => {
  const { id } = useParams(); // получаем ID редактируемого предмета
  const navigate = useNavigate();
  const [itemTypes, setItemTypes] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    serial_number: '',
    inventory_number: '',
    item_type: '',
    description: '',
    purchase_date: '',
    cost: '',
    is_active: true,
  });
  const [error, setError] = useState('');

  // Получаем данные редактируемого предмета
  useEffect(() => {
    api.get(`inventory-items/${id}/`)
      .then(response => {
        // Обратите внимание: если API возвращает item_type как объект или ID,
        // подстроим форму соответственно. Здесь предполагаем, что возвращается ID.
        setFormData(response.data);
      })
      .catch(err => {
        console.error('Ошибка получения данных предмета:', err);
      });
  }, [id]);

  // Получаем список типов предметов для выпадающего списка
  useEffect(() => {
    api.get('item-types/')
      .then(response => setItemTypes(response.data))
      .catch(err => console.error('Ошибка получения типов:', err));
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Отправляем PUT-запрос для обновления предмета
    api.put(`inventory-items/${id}/`, formData)
      .then(response => {
        // После успешного обновления перенаправляем пользователя на страницу деталей
        navigate(`/item/${id}`);
      })
      .catch(err => {
        console.error('Ошибка обновления предмета:', err);
        setError('Ошибка обновления предмета.');
      });
  };

  return (
    <div>
      <h2>Редактирование предмета</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Название: </label>
          <input 
            type="text" 
            name="name" 
            value={formData.name} 
            onChange={handleChange} 
            required 
          />
        </div>
        <div>
          <label>Серийный номер: </label>
          <input 
            type="text" 
            name="serial_number" 
            value={formData.serial_number} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>Инвентарный номер: </label>
          <input 
            type="text" 
            name="inventory_number" 
            value={formData.inventory_number} 
            onChange={handleChange} 
            required
          />
        </div>
        <div>
          <label>Тип предмета: </label>
          <select 
            name="item_type" 
            value={formData.item_type} 
            onChange={handleChange} 
            required
          >
            <option value="">Выберите тип</option>
            {itemTypes.map(type => (
              <option key={type.id} value={type.id}>
                {type.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label>Описание: </label>
          <textarea 
            name="description" 
            value={formData.description} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>Дата покупки: </label>
          <input 
            type="date" 
            name="purchase_date" 
            value={formData.purchase_date || ''} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>Стоимость: </label>
          <input 
            type="number" 
            step="0.01" 
            name="cost" 
            value={formData.cost} 
            onChange={handleChange} 
          />
        </div>
        <div>
          <label>Активен: </label>
          <input 
            type="checkbox" 
            name="is_active" 
            checked={formData.is_active} 
            onChange={handleChange} 
          />
        </div>
        <button type="submit">Сохранить изменения</button>
      </form>
    </div>
  );
};

export default EditItemPage;
