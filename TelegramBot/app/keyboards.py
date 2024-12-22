# keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import (
    SHOW_EVENTS_BUTTON,
    ADD_PLAYLIST_BUTTON,
    CHANGE_CITY_BUTTON,
    BACK_BUTTON_TEXT,
    SHOW_EVENTS_CALLBACK,
    ADD_PLAYLIST_CALLBACK,
    CHANGE_CITY_CALLBACK,
    CITY_MOSCOW,
    CITY_SAINT_PETERSBURG,
    CITY_NOVOSIBIRSK,
    CITY_YEKATERINBURG,
    CITY_KAZAN,
    CITY_NIZHNIY_NOVGOROD,
    CITY_CHELYABINSK,
    CITY_SAMARA,
    CITY_UFA,
    CITY_OTHER,
    CITY_MOSCOW_CALLBACK,
    CITY_SAINT_PETERSBURG_CALLBACK,
    CITY_NOVOSIBIRSK_CALLBACK,
    CITY_YEKATERINBURG_CALLBACK,
    CITY_KAZAN_CALLBACK,
    CITY_NIZHNIY_NOVGOROD_CALLBACK,
    CITY_CHELYABINSK_CALLBACK,
    CITY_SAMARA_CALLBACK,
    CITY_UFA_CALLBACK,
    CITY_OTHER_CALLBACK
)

# Клавиатура для приветственного сообщения
intro_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=SHOW_EVENTS_BUTTON,
                callback_data=SHOW_EVENTS_CALLBACK
            )
        ],
        [
            InlineKeyboardButton(
                text=ADD_PLAYLIST_BUTTON,
                callback_data=ADD_PLAYLIST_CALLBACK
            ),
            InlineKeyboardButton(
                text=CHANGE_CITY_BUTTON,
                callback_data=CHANGE_CITY_CALLBACK
            )
        ]
    ]
)

# Клавиатура для сообщения с просьбой добавить плейлист
add_playlist_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BACK_BUTTON_TEXT,
                callback_data="back_to_intro"
            )
        ]
    ]
)

# Клавиатура для выбора города с кнопкой "Назад"
change_city_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=CITY_MOSCOW, callback_data=CITY_MOSCOW_CALLBACK),
            InlineKeyboardButton(text=CITY_SAINT_PETERSBURG, callback_data=CITY_SAINT_PETERSBURG_CALLBACK),
            InlineKeyboardButton(text=CITY_NOVOSIBIRSK, callback_data=CITY_NOVOSIBIRSK_CALLBACK)
        ],
        [
            InlineKeyboardButton(text=CITY_YEKATERINBURG, callback_data=CITY_YEKATERINBURG_CALLBACK),
            InlineKeyboardButton(text=CITY_KAZAN, callback_data=CITY_KAZAN_CALLBACK),
            InlineKeyboardButton(text=CITY_NIZHNIY_NOVGOROD, callback_data=CITY_NIZHNIY_NOVGOROD_CALLBACK)
        ],
        [
            InlineKeyboardButton(text=CITY_CHELYABINSK, callback_data=CITY_CHELYABINSK_CALLBACK),
            InlineKeyboardButton(text=CITY_SAMARA, callback_data=CITY_SAMARA_CALLBACK),
            InlineKeyboardButton(text=CITY_UFA, callback_data=CITY_UFA_CALLBACK)
        ],
        [
            InlineKeyboardButton(text=CITY_OTHER, callback_data=CITY_OTHER_CALLBACK)
        ],
        [
            InlineKeyboardButton(
                text=BACK_BUTTON_TEXT,
                callback_data="back_to_intro"
            )
        ]
    ]
)
