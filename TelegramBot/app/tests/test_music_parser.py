import os
import sys

import pytest
from unittest.mock import patch, Mock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from music_parser import YMusicUser, process_playlist


# Проверка на правильный парсинг и получения ID
@patch('music_parser.Client')
def test_extract_user_and_playlist_id(mock_client):
    url = "https://music.yandex.ru/users/testuser/playlists/123"
    playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)
    assert playlist_id == "123"
    assert user_id == "testuser"


# Проверка на неправильную ссылку
def test_extract_user_and_playlist_id_invalid():
    url = "invalid_url"
    playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)
    assert playlist_id is None
    assert user_id is None
