import requests
from bs4 import BeautifulSoup

HOST = 'https://music.yandex.ru/'
URL = 'https://music.yandex.ru/users/robertchechenov/playlists/3'

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}


def get_HTML(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='d-track')
    songs = []
    for item in items:
        songs.append(
            {
                'title': item.find('a', class_='d-track__title').get_text()
                #'artist': item.find('div', class_='d-track__meta').get_text()
            }
        )
    print(songs)


html = get_HTML(URL)d-track__meta
get_content(html.text)

fetch("https://music.yandex.ru/handlers/playlist.jsx?owner=robertchechenov&kinds=3&light=true&madeFor=&withLikesCount=true&forceLogin=true&lang=ru&external-domain=music.yandex.ru&overembed=false&ncrnd=0.6843935294861014", {
  "headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-current-uid": "1371045360",
    "x-requested-with": "XMLHttpRequest",
    "x-retpath-y": "https://music.yandex.ru/users/robertchechenov/playlists/3",
    "x-yandex-music-client-now": "2024-11-24T14:43:32+03:00",
    "cookie": "yandexuid=6349545711718863547; yashr=7007781871718863547; yuidss=6349545711718863547; ymex=2034223547.yrts.1718863547; i=PJUXSXXkEuDb+57N+W1ru6pdp4OqOdu3fLP5dv06XV7lciicDWS9SjZjTeY9FRL3lshH5I2JCeIBt6cbEFlEfbRKs+0=; yp=2046815535.udn.cDpyb2JlcnRjaGVjaGVub3Y%3D; L=W1RhVXtVYWRJcgFXcVlob3BaDAxYYX5fRFYtBBhCNjkBECEsPD1O.1731455535.15949.324742.9d4eb47bc9b9a3f09bf282817b0f4632; yandex_login=robertchechenov; allow_next=true; chromecast=''; device_id=a0c1169a2f44c2029118f18598c17f9d560abc613; Session_id=3:1732446151.5.0.1731455535743:Wx0fLg:fd0b.1.2:1|1371045360.0.2.3:1731455535|3:10298693.596418.GZgdfIVEp_NxS_1BU4ub4WuAClY; sessar=1.1196.CiCvm_ckHwm-4McYqS8wOoPcJPe7DDVeKyrN5ePwvGHJHQ.59y0TZJIDUvViwnjQ37RP7uc1S-TAUoKPA_dHKNGeL0; sessionid2=3:1732446151.5.0.1731455535743:Wx0fLg:fd0b.1.2:1|1371045360.0.2.3:1731455535|3:10298693.596418.fakesign0000000000000000000; _yasc=ADyBm2xBsSxMbdI2pc41pA2myy86AsNfTu2M9NiVXeAwgkrzJq1bQ4ECEo5FgxZaOaqmoFb/+n369WA=; spravka=dD0xNzMyNDQ2NjM5O2k9ODEuMjAwLjE3LjEwNztEPTQzRTU3MzNFMkZDNERFMzY1RDZGOTlBRDAxRjJGQkUwM0M4Nzg2MkNCMzY2MzgxMTRFQjRCNDZBNzBCRDJENDJFMUVBODNDNzlBNTkxQ0IxMzVCNTFBQUNDN0ZGNkU4MTBGMzBERjJEQ0FEREIwMDBBMTZGQjhFNDkxMkUwMzY3NDI3Qjc4MUUwRDQ0MzQ1NTI0RTJFREFCMEY0M0I4QkIzM0EzNUZFQ0NERkZFMzkxN0I4QzExODQ5ODt1PTE3MzI0NDY2Mzk3MDY4NTI4Mjg7aD01NGVmYjZhY2M0ZGE2ZTNhYWQ2OTI2YTU2MmFhZjc5NQ==; bh=EkEiR29vZ2xlIENocm9tZSI7dj0iMTMxIiwgIkNocm9taXVtIjt2PSIxMzEiLCAiTm90X0EgQnJhbmQiO3Y9IjI0IioCPzA6ByJtYWNPUyJg+Z+MugZqIdzK0bYBu/GfqwT61obMCNLR7esD/Lmv/wff/ZPhBPOBAg==; active-browser-timestamp=1732448605099; lastVisitedPage=%7B%221371045360%22%3A%22%2Fusers%2Frobertchechenov%2Fplaylists%22%7D",
    "Referer": "https://music.yandex.ru/users/robertchechenov/playlists/3",
    "Referrer-Policy": "no-referrer-when-downgrade"
  },
  "body": null,
  "method": "GET"
});