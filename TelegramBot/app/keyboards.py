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

# Клавиатура для назад
back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BACK_BUTTON_TEXT,
                callback_data="back_to_intro"
            )
        ]
    ]
)
