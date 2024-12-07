import os
from re import search

from dotenv import load_dotenv
from yandex_music import Client


class YMusicUser:
    def __init__(self):
        load_dotenv()
        token = os.getenv('YMUSIC_TOKEN')
        self.client = Client(token).init()

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

    #Не работает токен одного аккаунта, токен другого аккаунта
    def get_concert(self, artist_id):
        artist = self.client.artists_brief_info(artist_id)
        return artist.concerts


url = "https://music.yandex.ru/users/Mr.Arslan004/playlists/1063?utm_medium=copy_link"
user = YMusicUser()
ids = user.get_artists(*YMusicUser.extract_user_and_playlist_id(url))
print(ids)
for id in ids:
    print(id, end=' ')
    print(user.get_concert(id))

