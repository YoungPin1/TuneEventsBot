from datetime import datetime
from aiogram.types import Message

from config import SessionLocal
from models import *


def is_user_registered(message: Message) -> bool:
    user_telegram_id = message.from_user.id
    # Открываем сессию для работы с базой данных
    with SessionLocal() as session:
        # Ищем пользователя по его telegram_id
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()

        # Если пользователя нет, создаем нового
        if not user:
            user = User(user_telegram_id=user_telegram_id,
                        city="Не указан")  # Создаем нового пользователя с городом "Не указан"
            session.add(user)
            session.commit()  # Сохраняем пользователя в базе данных
            return False
        return True


def add_users_city(user_telegram_id, new_city) -> None:
    city_name = new_city
    with SessionLocal() as session:
        # Ищем пользователя по его telegram_id
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        # Если пользователь найден, обновляем его город
        if user:
            user.city = city_name  # Обновляем город
            session.commit()  # Сохраняем изменения в базе данных
        else:
            print(f"Пользователь с ID {user_telegram_id} не найден.")


def add_artist_and_concert_to_db(concert_data: dict, user_telegram_id: int):
    try:
        with SessionLocal() as session:
            # Проверяем, существует ли пользователь
            user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
            if not user:
                print(f"Пользователь с ID {user_telegram_id} не найден в базе.")
                return

            # Извлекаем данные о концерте
            artist_name = str(concert_data['artist_id'])  # Предполагается, что artist_name передается в concert_data
            concert_date = datetime.strptime(concert_data['datetime'].split('+')[0], "%Y-%m-%dT%H:%M:%S")
            concert_city = concert_data['city']
            concert_title = concert_data['concert_title']
            place = concert_data.get('place', None)
            address = concert_data.get('address', None)
            afisha_url = concert_data.get('afisha_url', None)

            # Проверяем, существует ли артист
            artist = session.query(Artist).filter_by(artist_name=artist_name).first()
            if not artist:
                # Если артиста нет, создаем его
                artist = Artist(artist_name=artist_name)
                session.add(artist)
                session.commit()

            # Проверяем, существует ли концерт
            concert = session.query(Concert).filter_by(
                concert_date=concert_date,
                concert_city=concert_city,
                concert_title=concert_title
            ).first()

            if not concert:
                # Если концерта нет, добавляем его
                concert = Concert(
                    concert_date=concert_date,
                    concert_city=concert_city,
                    concert_title=concert_title,
                    place=place,
                    address=address,
                    afisha_url=afisha_url
                )
                session.add(concert)
                session.commit()

            # Проверяем и создаем связь между артистом и концертом
            artist_concert_link = session.query(artists_concerts).filter_by(
                artist_id=artist.artist_id,
                concert_id=concert.concert_id
            ).first()

            if not artist_concert_link:
                # Если связи нет, добавляем её через промежуточную таблицу
                insert_statement = artists_concerts.insert().values(
                    artist_id=artist.artist_id,
                    concert_id=concert.concert_id
                )
                session.execute(insert_statement)
                session.commit()

            # Создаем связь между пользователем и концертом
            user_concert_link = session.query(UserConcerts).filter_by(
                user_id=user.user_id,
                concert_id=concert.concert_id
            ).first()

            if not user_concert_link:
                user_concert_link = UserConcerts(
                    user_id=user.user_id,
                    concert_id=concert.concert_id
                )
                session.add(user_concert_link)
                session.commit()

    except Exception as e:
        print(f"Ошибка при добавлении артиста и концертов: {e}")