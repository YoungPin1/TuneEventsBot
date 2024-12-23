import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from re import search

from dotenv import load_dotenv
from yandex_music import Client

from db_editor import add_artist_and_concert_to_db


class YMusicUser:
    def __init__(self, city=None):
        load_dotenv()
        token = os.getenv('YMUSIC_TOKEN')
        self.client = Client(token).init()
        self.city = city
        self.all_concerts = []

    @staticmethod
    def extract_user_and_playlist_id(url):
        pattern = r'https://music\.yandex\.ru/users/([^/]+)/playlists/(\d+)'
        match = search(pattern, url)
        if match:
            user = match.group(1)
            playlist_id = match.group(2)
            return playlist_id, user
        else:
            return None, None

    def get_artists(self, playlist_id, user_id):
        playlist = self.client.users_playlists(playlist_id, user_id)
        playlist_tracks = playlist.fetch_tracks()

        artist_ids = set()
        for track_short in playlist_tracks:
            for artist in track_short.track.artists:
                artist_ids.add(artist.id)
        return artist_ids

    def get_concert(self, artist_id):
        try:
            artist = self.client.artists_brief_info(artist_id)
            if not artist or not hasattr(artist, 'concerts'):
                print(f"Информация о концертах для артиста с ID {artist_id} недоступна.")
                return []
            concerts = artist.concerts
            return [concert for concert in concerts if
                    concert.get('city').lower().replace(" ", "").replace("-", "")
                    == self.city.lower().replace(" ", "").replace("-", "")]
        except Exception as e:
            print(f"Ошибка при получении информации об артисте с ID {artist_id}: {e}")
            return []


def process_playlist(url, city, user_telegram_id, new_upload_id):
    user = YMusicUser(city.lower())
    playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)

    if playlist_id and user_id:
        artist_ids = user.get_artists(playlist_id, user_id)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_artist = {executor.submit(user.get_concert, artist_id): artist_id for artist_id in artist_ids}

            for future in as_completed(future_to_artist):
                artist_id = future_to_artist[future]
                try:
                    concerts = future.result()
                    for concert in concerts:
                        concert_data = {
                            'artist_id': artist_id,
                            'concert_title': concert['concert_title'],
                            'datetime': concert['datetime'],
                            'city': concert.get('city', 'Не указан'),
                            'place': concert.get('place', None),
                            'address': concert.get('address', None),
                            'afisha_url': concert.get('afisha_url', None)
                        }
                        add_artist_and_concert_to_db(concert_data, user_telegram_id, new_upload_id)
                        # Вывод текущего upload_id
                        print(
                            f"Пользователь с ID {user_telegram_id} загрузил новый плейлист с upload_id {new_upload_id}.")
                        user.all_concerts.append(concert)
                except Exception as e:
                    print(f"Ошибка при обработке артиста с ID {artist_id}: {e}")

        return user.all_concerts
    else:
        print("Некорректная ссылка на плейлист.")
        return []
