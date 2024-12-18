<h1 align="center">🎵 концерт.пошли</h1>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-000000?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white)

</div>

---

<p align="center">
  ➡️➡️ <strong>Отчёт по проделанной работе к КТ-2</strong> ⬅️⬅️  
  <br><br>
  📄 <a href="./REPORT.md"><strong>Посмотреть отчёт</strong></a>
</p>

---


## 📄 Описание проекта

*Концерт.пошли* — это Telegram бот, который принимает ссылку на плейлист из Яндекс.Музыки, анализирует его, извлекает информацию о музыкантах, собирает информацию о предстоящих концертах этих музыкантов, формирует и отправляет график концертов пользователю Telegram.

## 🎯 Функциональность

### 1. Анализ плейлиста
Бот получает ссылку на плейлист из Яндекс.Музыки, анализирует его и извлекает данные о музыкантах, которые в нем представлены.

### 2. Сбор информации о концертах
Используя API Яндекс.Афиши и Яндекс.Музыки, бот собирает информацию о предстоящих концертах этих музыкантов.

### 3. Формирование графика
Бот формирует расписание всех ближайших концертов и отправляет его пользователю через Telegram (или другим выбранным способом).


## 🖥️ Пользовательский интерфейс (UI)

### Отправка ссылки
Пользователь вводит команду и отправляет ссылку на плейлист из Яндекс.Музыки. Бот анализирует плейлист и сохраняет музыкальные предпочтения пользователя для последующих рекомендаций и уведомлений.

### Получение расписания концертов
Бот присылает расписание концертов с информацией о местах проведения, датах и времени.

### Интерактивные команды
- **Настройка уведомлений**: Пользователь может настроить регулярные уведомления о предстоящих концертах.
- **Рекомендации**: Исходя из сохраненного плейлиста, бот предлагает концерты, которые могут заинтересовать пользователя.
- **Добавление и удаление городов**:Пользователь может добавлять города, где его интересуют концерты, и удалять те, которые более не актуальны.
- **Добавление и удаление исполнителей**: Пользователь может добавлять исполнителей для получения уведомлений и рекомендаций по их концертам, а также удалять их из списка.
- **Просмотр и удаление концертов из списка**: Бот дает возможность просматривать список сохраненных концертов и удалять те, которые уже не актуальны.

## 🏛️ Архитектура системы

![Диаграмма архитектуры](architecture-diagram.jpg)

### Пользователи
Пользователи взаимодействуют с ботом через Telegram. Их команды передаются в интерфейс бота посредством Telegram API.

### Сервер приложения
Сервер приложения — центральный компонент системы. Он принимает запросы от Telegram-бота, обрабатывает их и взаимодействует с базой данных для выполнения необходимых действий.

### База данных PostgreSQL
Хранит данные о пользователях, плейлистах, исполнителях и концертах.


## 🏗️ База данных
![Диаграмма архитектуры](dataBaseFinal.jpg)


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
- **PostgreSQL**: Управление базой данных для быстрого доступа к информации о концертах.
- **SQLAlchemy**: Использование ORM SQLAlchemy для удобной работы с данными.
- **Интеграция с Яндекс Музыкой**: Извлечение информации о плейлистах и исполнителях.
- **Уведомления**: Автоматическая система оповещений о новых концертах или изменениях в расписании.


## 👥 Команда разработчиков

| Валерий Убушаев 💻 | Роберт Чеченов 💻 | Сулейман Лугма 💻 | Арслан Батталов 💻 |
|:----------------:|:--------------:|:--------------:|:---------------:|
| [@flw1n](https://t.me/flw1n)<br>Развертывание БД, ORM SQLAlchemy<br>Разработчик | [@roberto_roz](https://t.me/roberto_roz)<br>Часть функционала, обработка взаимодействия с пользователем (плейлисты, исполнители)<br>Разработчик | [@lsuleimanl](https://t.me/lsuleimanl)<br>Связь с Яндекс Афишей (парсинг/api)<br>Разработчик | [@young_pin1](https://t.me/young_pin1)<br>Создание и развертывание бота, часть функционала<br>Разработчик |
