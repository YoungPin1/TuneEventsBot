<h1 align="center">🎵 концерт.пошли</h1>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-000000?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white)

</div>


## 📄 Описание проекта

*Концерт.пошли* — это Telegram бот, который принимает ссылку на плейлист из Яндекс Музыки, анализирует плейлист, извлекая информацию о музыкантах, собирает информацию о предстоящих концертах этих музыкантов, формирует и отправляет график концертов пользователю Telegram.

## 🎯 Функциональность

### 1. Получение ссылки на плейлист
Бот принимает ссылку на плейлист из Яндекс Музыки, анализирует его и извлекает информацию о музыкантах, представленных в плейлисте.

### 2. Анализ музыкантов
Бот выполняет анализ, используя технологии для распознавания и обработки имен исполнителей.

### 3. Сбор информации о концертах
Бот собирает данные о предстоящих концертах музыкантов, используя API Яндекс Афиши.

### 4. Формирование графика
Бот составляет расписание всех предстоящих мероприятий и отправляет его пользователю через Telegram (или другой указанный канал).

### 5. Рекомендации и поиск с использованием AI
Бот может давать рекомендации по похожим исполнителям и предоставлять расширенные поисковые возможности с использованием искусственного интеллекта. (optional)

## 🖥️ Пользовательский интерфейс (UI)

### Отправка ссылки
Пользователь вводит команду и отправляет ссылку на плейлист из Яндекс Музыки. Бот анализирует плейлист и сохраняет музыкальные предпочтения пользователя для дальнейших рекомендаций и уведомлений.

### Получение расписания концертов
Бот отправляет расписание концертов, включающее информацию о местах проведения, датах и времени.

### Интерактивные команды
- **Настройка уведомлений**: Пользователь может настроить регулярные уведомления о предстоящих концертах.
- **Рекомендации**: На основе сохраненного плейлиста бот предлагает рекомендации на концерты, которые могут быть интересны пользователю.
- **Добавление и удаление городов**: Пользователь может добавлять города, где его интересуют концерты, и удалять города, которые его больше не интересуют.
- **Добавление и удаление исполнителей**: Пользователь может добавлять исполнителей, чтобы получать уведомления и рекомендации по их концертам, а также удалять исполнителей.
- **Просмотр и удаление концертов из списка**: Бот позволяет пользователю просматривать список сохраненных концертов и удалять концерты, которые больше не актуальны.


## 🏛️ Архитектура системы

![Диаграмма архитектуры](architecture-diagram.jpg)

### Пользователи
Взаимодействуют с ботом через Telegram. Входные команды пользователей передаются в интерфейс (UI) бота через Telegram API.

### Сервер приложения
Является центральным компонентом архитектуры. Написан на Python и принимает запросы от Telegram бота, обрабатывает их, и взаимодействует с базой данных PostgreSQL для выполнения необходимых операций.

### База данных PostgreSQL
Хранит данные о пользователях, плейлистах, исполнителях и концертах.


## 🏗️ База данных
![Диаграмма архитектуры](data-base.jpg)


| Таблица          | Описание                                                                                   |
|------------------|--------------------------------------------------------------------------------------------|
| **User**         | Хранит данные пользователей (User_ID, User_Telegram_ID, City).                             |
| **Artists**      | Список всех исполнителей (Artist_ID, Artist_Name).                                         |
| **Concerts**     | Информация о концертах (Concert_ID, Artist_ID, Concert_Date, Concert_City).                 |
| **Artists_Users**| Связь пользователей с их любимыми музыкантами (Artists_Users_ID, User_ID, Artist_ID).       |
| **User_Concerts**| Информация о концертах, которые интересуют пользователей (User_Concerts_ID, User_ID, Concert_ID). |
| **Playlist**     | Форматированный импорт данных из плейлистов (например, CSV, XML, JSON).                    |

## ⚙️ Внутренняя логика и начинка

- **AIOGRAM**: Асинхронная обработка запросов пользователей и работа с Telegram API.
- **PostgreSQL**: Управление базой данных с быстрым доступом к концертной информации.
- **SQLAlchemy**: Использование ORM SQLAlchemy для удобной работы с данными.
- **Интеграция с Яндекс Музыкой**: Извлечение информации о плейлистах и исполнителях.
- **AI-модули (опционально)**: Улучшение пользовательского опыта через рекомендации музыки и адаптивный поиск.
- **Уведомления**: Автоматизированная система оповещений о новых концертах или изменениях в расписании.


## 👥 Команда разработчиков

| Валерий Убушаев 💻 | Роберт Чеченов 💻 | Сулейман Лугма 💻 | Арслан Батталов 💻 |
|:----------------:|:--------------:|:--------------:|:---------------:|
| [@flw1n](https://t.me/flw1n)<br>Развертывание БД, ORM SQLAlchemy<br>Разработчик | [@roberto_roz](https://t.me/roberto_roz)<br>Часть функционала, обработка взаимодействия с пользователем (плейлисты, исполнители)<br>Разработчик | [@lsuleimanl](https://t.me/lsuleimanl)<br>Связь с Яндекс Афишей (парсинг/api)<br>Разработчик | [@young_pin1](https://t.me/young_pin1)<br>Создание и развертывание бота, часть функционала<br>Разработчик |

