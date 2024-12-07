from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
# import locale

import keyboards as kb
from music_parser import process_playlist

router = Router()

# Устанавливаем локаль для русской даты
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


# Состояния для FSM
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
    await message.answer("🎵 Добавь свой первый плейлист!\n\n"
                         "Отправь ссылку на плейлист из Yandex Music, например:\n"
                         "<i>https://music.yandex.ru/users/username/playlists/123</i>",
                         parse_mode="HTML")


# Добавление первой ссылки
@router.message(Info.link)
async def add_first_link(message: Message, state: FSMContext) -> None:
    if message.text.startswith("https://music.yandex."):
        await state.update_data(link=message.text)
        await state.set_state(Info.city)
        await message.answer("🏙️ Введите город, в котором проживаете:")
    else:
        await message.answer("❌ Это не ссылка на плейлист из Yandex Music. Попробуйте снова.")


# Добавление города и отправка концертов
@router.message(Info.city)
async def add_first_city(message: Message, state: FSMContext) -> None:
    global current_concert_index
    data = await state.get_data()
    playlist_link = data.get('link')
    await state.update_data(city=message.text)

    concerts = process_playlist(playlist_link, message.text)
    await state.update_data(concerts=concerts)

    current_concert_index = 0
    await send_concert(message, concerts, current_concert_index)


# Функция отправки информации о концерте
async def send_concert(message: Message, concerts, index: int):
    concert = concerts[index]
    concertTitle = concert['concert_title']
    datetimeRaw = concert['datetime']
    place = concert['place']
    address = concert['address']
    afishaUrl = concert['afisha_url']

    datetimeStr = datetimeRaw.split('+')[0]
    formattedDate = datetime.strptime(datetimeStr, "%Y-%m-%dT%H:%M:%S").strftime("%d %B %Y, %H:%M")

    messageText = (
        f"🎤 <b>Артист:</b> {concertTitle}\n"
        f"📅 <b>Дата и время:</b> {formattedDate}\n"
        f"🏢 <b>Площадка:</b> {place}\n"
        f"📍 <b>Адрес:</b> {address}\n\n"
        f"Нажмите <a href=\"{afishaUrl}\">тык</a> для покупки билета 🎟️"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующее", callback_data="next_concert")]
        ]
    )

    await message.answer(messageText, parse_mode="HTML", reply_markup=keyboard)


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
        await callback.answer("Это был последний концерт!", show_alert=True)

    await callback.answer()


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
