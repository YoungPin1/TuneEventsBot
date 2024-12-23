from datetime import datetime

from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

import keyboards as kb
from config import SessionLocal
from constants import *
from models import *
from db_editor import is_user_registered, get_concerts_by_user_telegram_id
from music_parser import process_playlist
from aux_functions import checkCityInSet

# import locale

router = Router()


# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class Info(StatesGroup):
    link = State()
    city = State()
    artist = State()


current_concert_index = 0  # Глобальный индекс текущего концерта


# функция для отправки приветственного сообщения с клавиатурой
async def send_intro_message(message: Message):
    # await message.answer_sticker(STICKER_WELCOME)
    await message.answer(
        INTRO_MESSAGE_TEXT,
        reply_markup=kb.intro_keyboard
    )


# Команда /start
@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! 👋", parse_mode="HTML")
    is_user_registered(message)

    # Отправка приветственного сообщения с кнопками
    await send_intro_message(message)


# Обработчик кнопки "Добавить плейлист"
@router.callback_query(F.data == "add_playlist")
async def add_playlist_button_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Закрываем уведомление о нажатии кнопки

    await state.set_state(Info.link)
    try:
        await callback_query.message.edit_text(
            ADD_FIRST_PLAYLIST,
            reply_markup=kb.add_playlist_keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"{ERROR_EDIT_USER_MESSAGE} {e}")
        prompt_message = await callback_query.message.answer(
            ADD_FIRST_PLAYLIST,
            reply_markup=kb.add_playlist_keyboard,
            parse_mode="HTML"
        )
        await state.update_data(prompt_message_id=prompt_message.message_id)
    else:
        # Если редактирование удалось, сохраняем новое message_id
        await state.update_data(prompt_message_id=callback_query.message.message_id)


# Обработчик кнопки "Назад"
@router.callback_query(F.data == "back_to_intro")
async def back_to_intro_handler(callback_query: CallbackQuery):
    await callback_query.answer()  # Закрываем уведомление о нажатии кнопки

    # Попытка заменить сообщение на приветственное
    try:
        await callback_query.message.edit_text(
            INTRO_MESSAGE_TEXT,
            reply_markup=kb.intro_keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"{ERROR_EDIT_USER_MESSAGE} {e}")
        await callback_query.message.answer(
            INTRO_MESSAGE_TEXT,
            reply_markup=kb.intro_keyboard,
            parse_mode="HTML"
        )


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
    user_telegram_id = message.from_user.id
    process_playlist(playlist_link, message.text, user_telegram_id)
    concerts = get_concerts_by_user_telegram_id(user_telegram_id)
    await state.update_data(concerts=concerts)

    try:
        await waiting_message.delete()
    except Exception as e:
        print(f"{ERROR_DELETE_WAIT_MESSAGE} {e}")

    # Проверка города
    if not checkCityInSet(message.text):
        await message.answer(INVALID_CITY)
        # Повторно отправляем запрос на ввод города с клавиатурой для выбора
        prompt_message = await message.answer(ENTER_CITY_PROMPT)
        await state.update_data(prompt_message_id=prompt_message.message_id)
        return  # Останавливаем дальнейшее выполнение обработчика

    # Отправляем сообщение с концертами и сохраняем его message_id
    concerts_message = await message.answer(FAVORITE_ARTISTS_CONCERTS)
    await state.update_data(concerts_message_id=concerts_message.message_id)

    current_concert_index = 0
    await send_concert(message, concerts, current_concert_index)


# Присылаем концерты
async def send_concert(message: Message, concerts, index: int):
    concert = concerts[index]
    concertTitle = concert['concert_title']
    formattedDate = concert['datetime']
    place = concert['place']
    address = concert['address']
    afishaUrl = concert['afisha_url']

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

        # Удаляем сообщение "🎉 Вот концерты ваших любимых артистов:"
        concerts_message_id = data.get('concerts_message_id')
        if concerts_message_id:
            try:
                await callback.message.bot.delete_message(
                    chat_id=callback.message.chat.id,
                    message_id=concerts_message_id
                )
            except Exception as e:
                print(f"{ERROR_DELETE_PLAYLIST_REQUEST_MESSAGE} {e}")

        current_concert_index = 0
        await state.clear()

        # Заменяем текущее сообщение на приветственное сообщение
        try:
            await callback.message.edit_text(
                INTRO_MESSAGE_TEXT,
                reply_markup=kb.intro_keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            print(f"{ERROR_EDIT_USER_MESSAGE} {e}")
            # Если редактирование не удалось, отправляем новое сообщение
            await callback.message.answer(
                INTRO_MESSAGE_TEXT,
                reply_markup=kb.intro_keyboard,
                parse_mode="HTML"
            )

    await callback.answer()


# Обработчик кнопки "Что умеет бот"
@router.callback_query(F.data == "what_bot_can_do")
async def what_bot_can_do_handler(callback_query: CallbackQuery):
    await callback_query.answer()  # Закрываем уведомление о нажатии кнопки

    help_text = HELP_TEXT

    await callback_query.message.edit_text(
        help_text,
        reply_markup=kb.back_keyboard,
        parse_mode="HTML"
    )

# Обработчик добавления плейлиста в базу данных (если необходимо)
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
        await message.answer(PLAYLIST_SAVE_SUCCESS_MESSAGE)
    except Exception as e:
        # В случае ошибки выводим сообщение и логируем ошибку
        print(f"{ERROR_ADD_PLAYLIST} {e}")
        await message.answer(ERROR_ADD_PLAYLIST_TRY_AGAIN)

    # Очищаем состояние FSM
    await state.clear()
