import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const CreateItemPage = () => {
  const navigate = useNavigate();
  // Состояние для списка типов предметов, чтобы отобразить их в выпадающем списке
  const [itemTypes, setItemTypes] = useState([]);
  // Состояние для формы
  const [formData, setFormData] = useState({
    name: '',
    serial_number: '',
     inventory_number: '',
    item_type: '', // здесь мы будем хранить ID выбранного типа
    description: '',
    purchase_date: '',
    cost: '',
    is_active: true,
  });
  const [error, setError] = useState('');

  // При монтировании компонента получаем список доступных типов предметов
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
    // Отправляем данные формы на эндпоинт создания предмета
    api.post('inventory-items/', formData)
      .then(response => {
        // После успешного создания перенаправляем пользователя на Dashboard
        navigate('/');
      })
      .catch(err => {
        console.error('Ошибка создания предмета:', err);
        setError('Ошибка создания предмета.');
      });
  };

  return (
    <div>
      <h2>Добавить новый предмет инвентаря</h2>
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
          <label>Серийный номер: </label>
          <input 
            type="text" 
            name="serial_number" 
            value={formData.serial_number} 
            onChange={handleChange} 
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
            value={formData.purchase_date} 
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
        <button type="submit">Создать предмет</button>
      </form>
    </div>
  );
};

export default CreateItemPage;
