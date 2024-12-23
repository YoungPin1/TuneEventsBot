import os
import sys

import pytest
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from music_parser import YMusicUser, process_playlist

class TestYMusicUser(unittest.TestCase):

    @patch('your_module.Client')
    @patch('your_module.add_artist_and_concert_to_db')
    def setUp(self, mock_add_db, mock_client):
        # Mock the Yandex Music Client
        self.mock_client_instance = mock_client.return_value
        self.mock_client_instance.init.return_value = self.mock_client_instance

        # Initialize YMusicUser with a test city
        self.user = YMusicUser(city='TestCity')

    def test_extract_user_and_playlist_id_valid(self):
        url = 'https://music.yandex.ru/users/test_user/playlists/123456'
        playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)
        self.assertEqual(playlist_id, '123456')
        self.assertEqual(user_id, 'test_user')

    def test_extract_user_and_playlist_id_invalid(self):
        url = 'https://music.yandex.ru/invalid_url'
        playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)
        self.assertIsNone(playlist_id)
        self.assertIsNone(user_id)

    def test_get_artists(self):
        # Mock playlist and tracks
        mock_playlist = MagicMock()
        mock_track = MagicMock()
        mock_artist = MagicMock()
        mock_artist.id = 'artist_id_1'
        mock_track.track.artists = [mock_artist]
        mock_playlist.fetch_tracks.return_value = [mock_track]
        self.mock_client_instance.users_playlists.return_value = mock_playlist

        artist_ids = self.user.get_artists('playlist_id', 'user_id')
        self.assertIn('artist_id_1', artist_ids)

    def test_get_concert(self):
        # Mock artist info with concerts
        mock_artist = MagicMock()
        mock_concert = {'city': 'TestCity', 'concert_title': 'Test Concert'}
        mock_artist.concerts = [mock_concert]
        self.mock_client_instance.artists_brief_info.return_value = mock_artist

        concerts = self.user.get_concert('artist_id_1')
        self.assertEqual(len(concerts), 1)
        self.assertEqual(concerts[0]['concert_title'], 'Test Concert')

    @patch('your_module.add_artist_and_concert_to_db')
    def test_process_playlist(self, mock_add_db):
        # Mock methods
        with patch.object(YMusicUser, 'get_artists', return_value={'artist_id_1'}), \
             patch.object(YMusicUser, 'get_concert', return_value=[{'concert_title': 'Test Concert', 'datetime': '2023-01-01T20:00:00', 'city': 'TestCity'}]):

            concerts = process_playlist('https://music.yandex.ru/users/test_user/playlists/123456', 'TestCity', 'user_telegram_id')
            self.assertEqual(len(concerts), 1)
            self.assertEqual(concerts[0]['concert_title'], 'Test Concert')
            mock_add_db.assert_called_once()

if __name__ == '__main__':
    unittest.main()
