import os
import sys

import pytest
from unittest.mock import AsyncMock, patch, Mock
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from handlers import command_start_handler, add_first_link, send_concert, send_next_concert, Info


# Проверка изначальной работоспособности кода
@pytest.mark.asyncio
async def test_command_start_handler():
    message = AsyncMock(spec=Message)

    # мок message.from_user, потому что без него ничего не работает
    message.from_user = Mock()
    message.from_user.full_name = "Test User"

    message.answer = AsyncMock()

    state = AsyncMock(spec=FSMContext)

    await command_start_handler(message, state)

    message.answer.assert_any_call("Привет, <b>Test User</b>!")
    state.set_state.assert_called_once_with(Info.link)


# Проверка правильного добавления ссылки
@pytest.mark.asyncio
async def test_add_first_link_valid():
    message = AsyncMock(spec=Message)
    message.text = "https://music.yandex.ru/users/testuser/playlists/123"

    message.answer = AsyncMock()
    state = AsyncMock(spec=FSMContext)

    await add_first_link(message, state)
    state.update_data.assert_any_call(link=message.text)
    state.set_state.assert_called_once_with(Info.city)
    message.answer.assert_called_once_with("🏙️ Введите город, в котором проживаете:")


# Проверка на неправильную ссылку
@pytest.mark.asyncio
async def test_add_first_link_invalid():
    message = AsyncMock(spec=Message)
    message.text = "invalid_link"
    state = AsyncMock(spec=FSMContext)
    message.answer = AsyncMock()

    await add_first_link(message, state)

    message.answer.assert_called_once_with("❌ Это не ссылка на плейлист из Yandex Music. Попробуйте снова.")


# Проверка на конец списка концертов
@pytest.mark.asyncio
async def test_send_next_concert():
    callback = AsyncMock(spec=CallbackQuery)
    callback.message = AsyncMock(spec=Message)

    callback.answer = AsyncMock()
    state = AsyncMock(spec=FSMContext)
    state.get_data.return_value = {
        'concerts': [
            {
                'concert_title': 'Artist 1',
                'datetime': '2024-05-01T20:00:00',
                'place': 'Venue 1',
                'address': 'Address 1',
                'afisha_url': 'http://example.com'
            }
        ]
    }

    # Патчим функцию send_concert, чтобы она не выполнялась реально
    with patch('handlers.send_concert', new_callable=AsyncMock) as mock_send_concert:
        await send_next_concert(callback, state)

        mock_send_concert.assert_not_called()

        callback.answer.assert_any_call("Это был последний концерт!", show_alert=True)
        callback.answer.assert_any_call()
