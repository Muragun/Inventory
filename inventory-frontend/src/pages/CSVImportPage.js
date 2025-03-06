import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

const CSVImportPage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      setError('Пожалуйста, выберите CSV-файл.');
      return;
    }
    setError('');
    const formData = new FormData();
    formData.append('file', file);

    // Отправляем POST-запрос на эндпоинт импорта
    api.post('import/inventory/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
      .then((response) => {
        setMessage('Импорт успешно выполнен.');
        setError('');
        // Перенаправляем на Dashboard через 2 секунды (или можно сразу)
        setTimeout(() => navigate('/'), 2000);
      })
      .catch((err) => {
        console.error('Ошибка импорта CSV-файла:', err);
        setError('Ошибка импорта CSV-файла.');
      });
  };

  return (
    <div>
      <h2>Импорт данных из CSV</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit">Импортировать</button>
      </form>
    </div>
  );
};

export default CSVImportPage;
