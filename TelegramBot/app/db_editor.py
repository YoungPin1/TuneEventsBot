from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import SessionLocal
from models import *
from music_parser import process_playlist


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


def add_users_city(message: Message) -> None:
    city_name = message.text
    user_telegram_id = message.from_user.id
    with SessionLocal() as session:
        # Ищем пользователя по его telegram_id
        user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()
        # Если пользователь найден, обновляем его город
        if user:
            user.city = city_name  # Обновляем город
            session.commit()  # Сохраняем изменения в базе данных
        else:
            print(f"Пользователь с ID {user_telegram_id} не найден.")


async def add_playlist_to_db(message: Message, state: FSMContext) -> None:
    playlist_link = message.text
    user_telegram_id = message.from_user.id

    try:
        # Получаем список артистов из плейлиста
        artists = process_playlist(playlist_link, None)[1]
        # Создаем сессию для работы с базой данных
        with SessionLocal() as session:
            # Проверяем, есть ли пользователь в базе, если нет, то добавляем его
            user = session.query(User).filter_by(user_telegram_id=user_telegram_id).first()

            # Обрабатываем артистов
            for artist_name in artists:
                # Ищем артиста по имени в базе
                artist_name = str(artist_name)
                artist = session.query(Artist).filter_by(artist_name=artist_name).first()

                # Если артиста нет в базе, добавляем нового
                if not artist:
                    artist = Artist(artist_name=artist_name)
                    session.add(artist)
                    session.commit()  # Сохраняем нового артиста в базе

                # Проверяем, есть ли уже связь между пользователем и артистом
                link_exists = session.query(ArtistsUsers).filter_by(
                    user_id=user.user_id,
                    artist_id=artist.artist_id
                ).first()

                # Если связи нет, создаем её
                if not link_exists:
                    session.add(ArtistsUsers(user_id=user.user_id, artist_id=artist.artist_id))
                    session.commit()
        # Уведомляем пользователя, что плейлист успешно добавлен
        await message.answer("Плейлист успешно добавлен и артисты сохранены!")
    except Exception as e:
        # В случае ошибки выводим сообщение и логируем ошибку
        print(f"Ошибка при добавлении плейлиста: {e}")
        await message.answer("Произошла ошибка при добавлении плейлиста. Попробуйте снова.")

    # Очищаем состояние FSM
    await state.clear()

