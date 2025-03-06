# Inventory
Приложение для инвентарного учета в университете. Состоит из двух частей:
1. **Backend (Django + PostgreSQL)** в папке `inventory_app`
2. **Frontend (React)** в папке `inventory_frontend`

## 1. Запуск Backend

### Установка и настройка

1. Убедитесь, что у вас установлен Python 3.9+ и PostgreSQL (или вы можете настроить SQLite для быстрого старта).
2. Перейдите в папку `inventory_app`:
   ```bash
   cd inventory_app
Создайте виртуальное окружение и активируйте его:
python3 -m venv venv
source venv/bin/activate

(На Windows: venv\Scripts\activate)

Установите зависимости:

bash
Копировать
pip install -r requirements.txt
Настройте базу данных. По умолчанию настройки в settings.py указывают на PostgreSQL. Если хотите быстро протестировать на SQLite, измените настройки DATABASES в settings.py.

Выполните миграции:

bash
Копировать
python manage.py migrate
Создайте суперпользователя (при необходимости):

bash
Копировать
python manage.py createsuperuser

Запустите сервер:

bash
Копировать
python manage.py runserver
Откройте в браузере http://127.0.0.1:8000/admin/ для админки или http://127.0.0.1:8000/api/ для API.

2. Запуск Frontend
Перейдите в папку inventory_frontend:
bash
Копировать
cd ../inventory_frontend
Убедитесь, что у вас установлен Node.js (v16+).

Установите зависимости:
bash
Копировать
npm install
Запустите дев‑сервер:
bash
Копировать
npm start
Откройте в браузере http://localhost:3000. Фронтенд будет обращаться к бэкенду по адресу http://127.0.0.1:8000.
