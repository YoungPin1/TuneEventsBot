from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from constants import (
    SHOW_EVENTS_BUTTON,
    ADD_PLAYLIST_BUTTON,
    CHANGE_CITY_BUTTON,
    BACK_BUTTON_TEXT,
    SHOW_EVENTS_CALLBACK,
    ADD_PLAYLIST_CALLBACK,
    SUPPORT_BUTTON_TEXT,
    SUPPORT_BUTTON_URL,
    BOT_CAPABILITIES_BUTTON_TEXT,
    WHAT_BOT_CAN_DO_CALLBACK,
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
            )
        ],
        [
            InlineKeyboardButton(
                text=SUPPORT_BUTTON_TEXT,
                url=SUPPORT_BUTTON_URL  # Используем URL для перенаправления
            ),
            InlineKeyboardButton(
                text=BOT_CAPABILITIES_BUTTON_TEXT,
                callback_data=WHAT_BOT_CAN_DO_CALLBACK
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
