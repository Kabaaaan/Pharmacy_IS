# Pharmacy Information System

Информационная система для управления сетью аптек, разработанная в рамках учебной практики ПетрГУ.

## 📌 О проекте

Система состоит из:
- **Backend API** (FastAPI + SQLAlchemy)
- **Desktop приложения** (PyQt5)
- **Базы данных** (MySQL/PostgreSQL)

Основные функции:
- Учет лекарственных препаратов
- Управление рецептами
- Оформление заказов
- Аналитика продаж
- Управление поставками

## 🗄️ Проектирование БД

### Схема базы данных

![Database Schema](docs/images/СтруктураБД-1.JPG)
![Database Schema](docs/images/СтруктураБД-2.JPG)

Основные сущности:
- **Сотрудники** (Worker) - сотрудники сети аптек;
- **Лекарства** (Medicine) - информация о лекрствах (товарах);
- **Рецепты** (Recipe) - назначения врачей;
- **Заказы** (Order) - покупки клиентов;
- **Закупки** (Shipment) - закупки у поставщиков;
- **Аптеки** (Pharmacy) - аптеки.


## 🚀 Запуск проекта

### Необходимые компоненты
- Python 3.10+
- MySQL/PostgreSQL
- Poetry (для управления зависимостями)

### Установка
```bash
git clone https://github.com/Kabaaaan/Pharmacy_IS.git
cd Pharmacy_IS
```

### Настройка БД
1. Создайте файл `.env` в корне проекта:
```ini
DB_HOST=localhost
DB_USER=pharmacy_user
DB_PASSWORD=your_password
DB_DATABASE=pharmacy_db
```

2. Инициализируйте БД:
```bash
python src/api/database/init_db.py
```

### Запуск API
```bash
python src/api/main.py
```

### Запуск приложения
```bash
python src/app/main.py
```

## 👥 Разработчики
- https://github.com/Kabaaaan
- https://github.com/ulyagolova

## 📄 Лицензия
MIT License © 2025