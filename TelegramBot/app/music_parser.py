import os
from re import search

from dotenv import load_dotenv
from yandex_music import Client


class YMusicUser:
    def __init__(self, city=None):
        load_dotenv()
        token = os.getenv('YMUSIC_TOKEN')
        self.client = Client(token).init()
        self.city = city
        self.concerts = []

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
        artist = self.client.artists_brief_info(artist_id)
        concerts = artist.concerts
        for concert in concerts:
            if concert['city'] == self.city:
                self.concerts.append(concert)


def process_playlist(url, city):
    user = YMusicUser(city)
    playlist_id, user_id = YMusicUser.extract_user_and_playlist_id(url)
    if playlist_id and user_id:
        ids = user.get_artists(playlist_id, user_id)
        concerts = []
        for artist_id in ids:
            concerts.append(user.get_concert(artist_id))
        print(user.concerts)
    else:
        print("Некорректная ссылка на плейлист.")
