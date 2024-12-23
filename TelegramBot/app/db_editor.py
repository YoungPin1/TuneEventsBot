from aiogram.types import Message

from config import SessionLocal
from models import *
from sqlalchemy import func


def is_user_registered(message: Message) -> bool:
    user_telegram_id = message.from_user.id
    # Открываем сессию для работы с базой данных
    session = SessionLocal()
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
    session = SessionLocal()
    # Ищем пользователя по его telegram_id
    user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
    # Если пользователь найден, обновляем его город
    if user:
        user.city = city_name  # Обновляем город
        session.commit()  # Сохраняем изменения в базе данных
    else:
        print(f"Пользователь с ID {user_telegram_id} не найден.")


def add_artist_and_concert_to_db(concert_data: dict, user_telegram_id: int, current_upload_id):
    try:
        session = SessionLocal()
        # Проверяем, существует ли пользователь
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        if not user:
            print(f"Пользователь с ID {user_telegram_id} не найден в базе.")
            return

        # Извлекаем данные о концерте
        artist_name = str(concert_data['artist_id'])
        concert_date = concert_data['datetime']
        concert_city = concert_data['city']
        concert_title = concert_data['concert_title']
        place = concert_data.get('place', None)
        address = concert_data.get('address', None)
        afisha_url = concert_data.get('afisha_url', None)

        # Проверяем, существует ли артист
        artist = session.query(Artist).filter_by(artist_name=artist_name).first()
        if not artist:
            artist = Artist(artist_name=artist_name)
            session.add(artist)
            session.commit()

        # Проверяем, существует ли концерт
        concert = session.query(Concert).filter_by(
            concert_date=concert_date,
            concert_city=concert_city,
            concert_title=concert_title,
            place=place,
            address=address,
            afisha_url=afisha_url
        ).first()
        if not concert:
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
            insert_statement = artists_concerts.insert().values(
                artist_id=artist.artist_id,
                concert_id=concert.concert_id
            )
            session.execute(insert_statement)
            session.commit()

        # Создаем или обновляем связь между пользователем и концертом
        user_concert_link = session.query(UserConcerts).filter_by(
            user_id=user.user_id,
            concert_id=concert.concert_id
        ).first()
        if user_concert_link:
            # Если связь уже существует, обновляем upload_id
            user_concert_link.upload_id = current_upload_id
        else:
            # Если связи нет, создаем новую
            user_concert_link = UserConcerts(
                user_id=user.user_id,
                concert_id=concert.concert_id,
                upload_id=current_upload_id
            )
            session.add(user_concert_link)

        session.commit()


    except Exception as e:
        print(f"Ошибка при добавлении артиста и концертов: {e}")


# Функция для получения концертов по user_telegram_id и upload_id
def get_concerts_by_user_telegram_id(user_telegram_id: int, upload_id: int) -> list[dict]:
    try:
        session = SessionLocal()
        # Получаем пользователя по его Telegram ID
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        if not user:
            print(f"Пользователь с Telegram ID {user_telegram_id} не найден.")
            return []
        # Фильтруем концерты по user_id и upload_id
        user_concerts = session.query(UserConcerts).filter_by(user_id=user.user_id, upload_id=upload_id).all()
        if not user_concerts:
            print(f"Концерты для пользователя с ID {user_telegram_id} и upload_id {upload_id} не найдены.")
            return []

        concerts_list = []
        for user_concert in user_concerts:
            concert = user_concert.concert
            if not concert:
                continue

            concert_data = {
                "concert_title": concert.concert_title,
                "datetime": concert.concert_date,
                "place": concert.place,
                "address": concert.address,
                "afisha_url": concert.afisha_url
            }
            concerts_list.append(concert_data)

        return concerts_list

    except Exception as e:
        print(f"Ошибка при получении концертов для пользователя: {e}")
        return []


def delete_user_concerts_by_user_telegram_id(user_telegram_id: int) -> None:
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        session.query(UserConcerts).filter_by(user_id=user.user_id).delete()
        session.commit()
        print(f"Записи для пользователя с ID {user_telegram_id} успешно удалены.")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при удалении записей для пользователя: {e}")


def get_all_concerts_by_user_telegram_id(user_telegram_id: int) -> list[dict]:
    try:
        session = SessionLocal()
        # Получаем пользователя по его Telegram ID
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        if not user:
            print(f"Пользователь с Telegram ID {user_telegram_id} не найден.")
            return []

        # Фильтруем концерты по user_id
        user_concerts = session.query(UserConcerts).filter_by(user_id=user.user_id).all()
        if not user_concerts:
            print(f"Концерты для пользователя с ID {user_telegram_id} не найдены.")
            return []

        concerts_list = []
        for user_concert in user_concerts:
            concert = user_concert.concert
            if not concert:
                continue

            concert_data = {
                "concert_title": concert.concert_title,
                "datetime": concert.concert_date,
                "place": concert.place,
                "address": concert.address,
                "afisha_url": concert.afisha_url
            }
            concerts_list.append(concert_data)

        return concerts_list

    except Exception as e:
        print(f"Ошибка при получении концертов для пользователя: {e}")
        return []

def get_last_upload_id_by_user_telegram_id(user_telegram_id: int) -> int:
    try:
        session = SessionLocal()
        # Получаем пользователя по его Telegram ID
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        if not user:
            print(f"Пользователь с Telegram ID {user_telegram_id} не найден.")
            return 0

        # Находим максимальный upload_id для пользователя
        max_upload_id = session.query(func.max(UserConcerts.upload_id)).filter_by(user_id=user.user_id).scalar()
        return max_upload_id or 0

    except Exception as e:
        print(f"Ошибка при получении последнего upload_id для пользователя: {e}")
        return 0