from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants import *

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
                text=CLEAN_PLAYLIST_BUTTON,
                callback_data=CLEAN_PLAYLIST_CALLBACK
            )
        ],
        [
            InlineKeyboardButton(
                text=SUPPORT_BUTTON_TEXT,
                url=SUPPORT_BUTTON_URL
            ),
            InlineKeyboardButton(
                text=BOT_CAPABILITIES_BUTTON_TEXT,
                callback_data=WHAT_BOT_CAN_DO_CALLBACK
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
                callback_data=BACK_BUTTON_CALLBACK
            )
        ]
    ]
)

# Клавиатура для отображения концертов с кнопками "Следующее" и "Назад"
concerts_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=NEXT_CONCERT_MESSAGE,
                callback_data=NEXT_CONCERT_CALLBACK
            )
        ],
        [
            InlineKeyboardButton(
                text=BACK_BUTTON_TEXT,
                callback_data=BACK_BUTTON_CALLBACK
            )
        ]
    ]
)
