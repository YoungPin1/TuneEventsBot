from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import re

import keyboards as kb
from music_parser import process_playlist

router = Router()


# ----------------------------------------------------------------------------------------------------------------------
# РЕГИСТРАЦИЯ
# ----------------------------------------------------------------------------------------------------------------------
class Info(StatesGroup):
    link = State()
    city = State()
    artist = State()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
    # запрашиваем ссылку на плейлист пользователя
    await state.set_state(Info.link)
    await message.answer("Добавь свой первый плейлист! (Отправь в чат ссылку на свой плейлист из Yandex Music)")


@router.message(Info.link)
async def add_first_link(message: Message, state: FSMContext) -> None:
    # Регулярное выражение для проверки ссылки на плейлист Yandex Music
    yandex_music_playlist_pattern = re.compile(
        r"^https?://music\.yandex\.(ru|com)/(users/[^/]+/playlists/\d+|album/\d+/track/\d+)$"
    )

    # Проверяем, соответствует ли ссылка шаблону
    if yandex_music_playlist_pattern.match(message.text):
        # Сохраняем ссылку на плейлист пользователя
        process_playlist(message.text)
        # Запрашиваем город пользователя
        await state.set_state(Info.city)
        await message.answer("Введите город, в котором проживаете)")
    else:
        # Сообщаем пользователю об ошибке и просим ввести ссылку ещё раз
        await message.answer(
            "Кажется, это не ссылка на плейлист из Yandex Music. Пожалуйста, отправьте корректную ссылку, например:\n\n"
            "https://music.yandex.ru/users/username/playlists/123"
        )


@router.message(Info.city)
async def add_first_city(message: Message, state: FSMContext) -> None:
    # сохраняем город пользователя
    await state.update_data(city=message.text)
    await state.clear()
    await message.answer("Доступные опции", reply_markup=kb.main)


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
