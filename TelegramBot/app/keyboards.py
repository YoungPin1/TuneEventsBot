from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Добавить Плейлист'), KeyboardButton(text='Удалить Плейлист')],
              [KeyboardButton(text='Добавить Город'), KeyboardButton(text='Удалить Город')],
              [KeyboardButton(text='Добавить Исполнителя'), KeyboardButton(text='Удалить Исполнителя')],
              [KeyboardButton(text='Посмотреть список Концертов'), KeyboardButton(text='Удалить Концерт из списка')]],
    resize_keyboard=True,
    input_field_placeholder='Выбирите пункт меню...')

reaction_on_artists = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Показать список Исполнителей', callback_data='get_artists')]])

reaction_on_cities = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Показать список Городов', callback_data='get_cities')]])
