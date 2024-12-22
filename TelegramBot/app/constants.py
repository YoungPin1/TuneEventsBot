ADD_FIRST_PLAYLIST = (
    "🎵 Добавь свой плейлист!\n\n"
    "Отправь ссылку на плейлист из Yandex Music, например:\n"
    "<i>https://music.yandex.ru/users/username/playlists/123</i>"
)

INTRO_MESSAGE_TEXT = (
    "🎉 Добро пожаловать в концерт.пошли! 🎶\n\n"
    "Тот самый бот для поиска концертов. Мы покажем вам все яркие события от ваших любимых исполнителей по вашей Яндекс Музыке. "
    "Не упустите шанс быть в курсе самых горячих концертов! 🔥\n\n"
    "Выберите действие ниже, чтобы начать:"
)


CONCERT_MESSAGE_TEMPLATE = (
    "{counter_text}"
    "🎤 <b>Артист:</b> {concert_title}\n"
    "📅 <b>Дата и время:</b> {formatted_date}\n"
    "🏢 <b>Площадка:</b> {place}\n"
    "📍 <b>Адрес:</b> {address}\n\n"
    "Нажмите <a href=\"{afisha_url}\">тык</a> для покупки билета 🎟️"
)

ERROR_EDIT_USER_MESSAGE = "Ошибка при редактировании сообщения:"
ERROR_DELETE_USER_MESSAGE = "Ошибка при удалении сообщения пользователя:"
ERROR_DELETING_PLAYLIST_REQUEST_MESSAGE = 'Ошибка при удалении сообщения с запросом плейлиста:'
ERROR_DELETING_USER_PLAYLIST_MESSAGE = 'Ошибка при удалении сообщения пользователя с плейлистом:'
ERROR_DELETE_CITY_REQUEST = "Ошибка при удалении сообщения с запросом города:"
SEARCH_CONCERTS_WAIT = "⏳ Подождите, идёт поиск концертов..."
ERROR_DELETE_WAIT_MESSAGE = "Ошибка при удалении сообщения об ожидании:"

FAVORITE_ARTISTS_CONCERTS = "🎉 Вот концерты ваших любимых артистов:"
WAIT_CONCERT_SEARCH = "⏳ Подождите, идёт поиск концертов..."
ENTER_CITY_PROMPT = "🏙️ Введите город, в котором проживаете:"
INVALID_PLAYLIST_LINK = "❌ Это не ссылка на плейлист из Yandex Music. Попробуйте снова."
NEXT_CONCERT_MESSAGE = '➡️ Следующее'
LAST_CONCERT_MESSAGE = "Это был последний концерт!"

SHOW_EVENTS_BUTTON = "📅 Показать мои события"
ADD_PLAYLIST_BUTTON = "➕ Добавить плейлист"
CHANGE_CITY_BUTTON = "🌍 Изменить город"
BACK_BUTTON_TEXT = "⬅️ Назад"

# Callback data для кнопок
SHOW_EVENTS_CALLBACK = "show_events"
ADD_PLAYLIST_CALLBACK = "add_playlist"
CHANGE_CITY_CALLBACK = "change_city"

CITY_MOSCOW = "Москва"
CITY_SAINT_PETERSBURG = "Санкт-Петербург"
CITY_NOVOSIBIRSK = "Новосибирск"
CITY_YEKATERINBURG = "Екатеринбург"
CITY_KAZAN = "Казань"
CITY_NIZHNIY_NOVGOROD = "Нижний Новгород"
CITY_CHELYABINSK = "Челябинск"
CITY_SAMARA = "Самара"
CITY_UFA = "Уфа"
CITY_OTHER = "Другой город"

# Callback data для городов
CITY_MOSCOW_CALLBACK = "city_moscow"
CITY_SAINT_PETERSBURG_CALLBACK = "city_saint_petersburg"
CITY_NOVOSIBIRSK_CALLBACK = "city_novosibirsk"
CITY_YEKATERINBURG_CALLBACK = "city_yekaterinburg"
CITY_KAZAN_CALLBACK = "city_kazan"
CITY_NIZHNIY_NOVGOROD_CALLBACK = "city_nizhny_novgorod"
CITY_CHELYABINSK_CALLBACK = "city_chelyabinsk"
CITY_SAMARA_CALLBACK = "city_samara"
CITY_UFA_CALLBACK = "city_ufa"
CITY_OTHER_CALLBACK = "city_other"

citySet = ('Москва')