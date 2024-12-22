from datetime import datetime

from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import SessionLocal
from models import *

import keyboards as kb
from constants import *
from music_parser import process_playlist

# import locale

router = Router()


# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class Info(StatesGroup):
    link = State()
    city = State()
    artist = State()


current_concert_index = 0  # Глобальный индекс текущего концерта


# Команда /start
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
    await state.set_state(Info.link)

    prompt_message = await message.answer(ADD_FIRST_PLAYLIST)
    await state.update_data(prompt_message_id=prompt_message.message_id)


# Обрабатываем ссылку на плейлист
@router.message(Info.link)
async def add_first_link(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    prompt_message_id = data.get('prompt_message_id')

    if prompt_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)
        except Exception as e:
            print(f"{ERROR_DELETING_PLAYLIST_REQUEST_MESSAGE} {e}")

    try:
        await message.delete()
    except Exception as e:
        print(f"{ERROR_DELETING_USER_PLAYLIST_MESSAGE} {e}")

    if message.text.startswith("https://music.yandex."):
        await state.update_data(link=message.text)
        await state.set_state(Info.city)

        prompt_message = await message.answer(ENTER_CITY_PROMPT)
        await state.update_data(prompt_message_id=prompt_message.message_id)
    else:
        await message.answer(INVALID_PLAYLIST_LINK)


# Добавляем город для поиска
@router.message(Info.city)
async def add_first_city(message: Message, state: FSMContext) -> None:
    global current_concert_index

    data = await state.get_data()
    prompt_message_id = data.get('prompt_message_id')
    if prompt_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)
        except Exception as e:
            print(f"{ERROR_DELETE_CITY_REQUEST} {e}")

    try:
        await message.delete()
    except Exception as e:
        print(f"{ERROR_DELETE_USER_MESSAGE} {e}")

    waiting_message = await message.answer(WAIT_CONCERT_SEARCH)
    playlist_link = data.get('link')
    await state.update_data(city=message.text)
    concerts = process_playlist(playlist_link, message.text)[0]
    await state.update_data(concerts=concerts)

    try:
        await waiting_message.delete()
    except Exception as e:
        print(f"{ERROR_DELETE_WAIT_MESSAGE} {e}")

    await message.answer(FAVORITE_ARTISTS_CONCERTS)

    current_concert_index = 0
    await send_concert(message, concerts, current_concert_index)


# Присылаем концерты
async def send_concert(message: Message, concerts, index: int):
    concert = concerts[index]
    concertTitle = concert['concert_title']
    datetimeRaw = concert['datetime']
    place = concert['place']
    address = concert['address']
    afishaUrl = concert['afisha_url']

    datetimeStr = datetimeRaw.split('+')[0]
    formattedDate = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S").strftime("%d %B %Y, %H:%M")

    total_concerts = len(concerts)
    counter_text = f"<b>{index + 1} из {total_concerts}</b>\n\n"

    messageText = CONCERT_MESSAGE_TEMPLATE.format(
        counter_text=counter_text,
        concert_title=concertTitle,
        formatted_date=formattedDate,
        place=place,
        address=address,
        afisha_url=afishaUrl
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=NEXT_CONCERT_MESSAGE, callback_data="next_concert")]
        ]
    )

    sent_message = await message.answer(messageText, parse_mode="HTML", reply_markup=keyboard)

    try:
        await message.delete()
    except Exception as e:
        print(f"{ERROR_DELETE_USER_MESSAGE} {e}")


# Обработчик кнопки "Следующее"
@router.callback_query(lambda c: c.data == "next_concert")
async def send_next_concert(callback: CallbackQuery, state: FSMContext):
    global current_concert_index
    data = await state.get_data()
    concerts = data.get('concerts', [])

    if current_concert_index < len(concerts) - 1:
        current_concert_index += 1
        await send_concert(callback.message, concerts, current_concert_index)
    else:
        await callback.answer(LAST_CONCERT_MESSAGE, show_alert=True)

    await callback.answer()

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
            if not user:
                user = User(user_telegram_id=user_telegram_id, city="Не указан")  # Или запросить город позже
                session.add(user)
                session.commit()

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


# ________

# рабочий старый код (отправляет все концерты разом)
# @router.message(Info.city)
# async def add_first_city(message: Message, state: FSMContext) -> None:
#     # сохраняем город пользователя
#     data = await state.get_data()
#     playlist_link = data.get('link')
#     await state.update_data(city=message.text)
#     concerts = process_playlist(playlist_link, message.text)
#     for concert in concerts:
#         print(concert)
#         concertTitle = concert['concert_title']
#         datetimeRaw = concert['datetime']
#         place = concert['place']
#         address = concert['address']
#         afishaUrl = concert['afisha_url']
#
#         datetimeStr = datetimeRaw.split('+')[0]
#         formattedDate = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S").strftime("%d %B %Y, %H:%M")
#
#         messageText = (
#             f"{'🎤 Артист:'} {concertTitle}\n"
#             f"{'📅 Дата и время:'} {formattedDate}\n"
#             f"{'🏢 Площадка:'} {place}\n"
#             f"{'📍 Адрес:'} {address}\n\n"
#             f"Нажмите <a href=\"{afishaUrl}\">тык</a> для покупки билета 🎟️"
#         )
#
#         await message.answer(messageText, parse_mode="HTML")
#     await state.clear()
#     await message.answer("Доступные опции", reply_markup=kb.main)


# ----------------------------------------------------------------------------------------------------------------------
# ДОБАВИТЬ / УДАЛИТЬ / ПОСМОТРЕТЬ ГОРОД(А)
# ----------------------------------------------------------------------------------------------------------------------
class City(StatesGroup):
    add_city = State()
    del_city = State()


@router.message(F.text == 'Добавить Город')
async def add_city_1(message: Message, state: FSMContext) -> None:
    # запрашиваем город пользователя
    await state.set_state(City.add_city)
    await message.answer("Введите город, в котором вам удобно посещать концерты)")


@router.message(F.text == 'Удалить Город')
async def del_city_1(message: Message, state: FSMContext) -> None:
    # запрашиваем город пользователя
    await state.set_state(City.del_city)
    await message.answer("Введите город, который хотите удалить из своего списка)")


@router.message(City.add_city)
async def add_city_2(message: Message, state: FSMContext) -> None:
    # сохраняем город пользователя
    await state.update_data(city=message.text)
    # добавить в базу данных
    await state.clear()
    await message.reply("Город Добавлен!")
    await message.answer("Доступна опция:", reply_markup=kb.reaction_on_cities)


@router.message(City.del_city)
async def del_city_2(message: Message, state: FSMContext) -> None:
    # сохраняем город пользователя
    await state.update_data(city=message.text)
    # удалить из базы данных
    await state.clear()
    await message.reply("Город Удален!")
    await message.answer("Доступна опция:", reply_markup=kb.reaction_on_cities)


@router.callback_query(F.data == 'get_cities')
async def returning_cities(callback: CallbackQuery) -> None:
    await callback.answer("2")
    await callback.message.answer("2")
    # тут будет информация из базы данных


# ----------------------------------------------------------------------------------------------------------------------
# ДОБАВИТЬ / УДАЛИТЬ / ПОСМОТРЕТЬ ИСПОЛНИТЕЛЯ(ЕЙ)
# ----------------------------------------------------------------------------------------------------------------------
class Artist(StatesGroup):
    add_artist = State()
    del_artist = State()


@router.message(F.text == 'Добавить Исполнителя')
async def add_artist_1(message: Message, state: FSMContext) -> None:
    # запрашиваем исполнителя пользователя
    await state.set_state(Artist.add_artist)
    await message.answer("Введите исполнителя, чьи концерты вы хотите видеть)")


@router.message(F.text == 'Удалить Исполнителя')
async def del_artist_1(message: Message, state: FSMContext) -> None:
    # запрашиваем исполнителя пользователя
    await state.set_state(Artist.del_artist)
    await message.answer("Введите исполнителя, который вам больше не интересен)")


@router.message(Artist.add_artist)
async def add_artist_2(message: Message, state: FSMContext) -> None:
    # сохраняем исполнителя пользователя
    await state.update_data(artist=message.text)
    # добавить в базу данных
    await state.clear()
    await message.reply("Исполнитель Добавлен!")
    await message.answer("Доступна опция:", reply_markup=kb.reaction_on_cities)


@router.message(Artist.del_artist)
async def del_artist_2(message: Message, state: FSMContext) -> None:
    # сохраняем исполнителя пользователя
    await state.update_data(artist=message.text)
    # удалить из базы данных
    await state.clear()
    await message.reply("Исполнитель Удален!")
    await message.answer("Доступна опция:", reply_markup=kb.reaction_on_artists)


@router.callback_query(F.data == 'get_artists')
async def returning_cities(callback: CallbackQuery) -> None:
    await callback.answer("1")
    await callback.message.answer("1")
    # тут будет информация из базы данных


# ----------------------------------------------------------------------------------------------------------------------
# ДОБАВИТЬ / УДАЛИТЬ ПЛЕЙЛИСТ(Ы)
# ----------------------------------------------------------------------------------------------------------------------
class PlayList(StatesGroup):
    add_playlist = State()
    del_playlist = State()


@router.message(F.text == 'Добавить Плейлист')
async def add_artist_1(message: Message, state: FSMContext) -> None:
    # запрашиваем плейлист пользователя
    await state.set_state(PlayList.add_playlist)
    await message.answer("Введите ссылку на Плейлист, исполнители которых вам интересны")


@router.message(F.text == 'Удалить Плейлист')
async def del_artist_1(message: Message, state: FSMContext) -> None:
    # запрашиваем плейлист пользователя
    await state.set_state(PlayList.del_playlist)
    await message.answer("Введите ссылку на Плейлист, концерты исполнителей которых вы не хотите посещать)")


@router.message(PlayList.add_playlist)
async def add_artist_2(message: Message, state: FSMContext) -> None:
    # сохраняем плейлист пользователя
    await state.update_data(artist=message.text)
    # добавить в базу данных
    await state.clear()
    await message.reply("Плейлист Добавлен!")


@router.message(PlayList.del_playlist)
async def del_artist_2(message: Message, state: FSMContext) -> None:
    # сохраняем плейлист пользователя
    await state.update_data(artist=message.text)
    # удалить из базы данных
    await state.clear()
    await message.reply("Плейлист Удален!")
