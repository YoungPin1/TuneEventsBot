from models import *

def checkCityInSet(cityName, citySet):
    # Преобразуем город в lowercase
    cityName = cityName.lower()

    # Проверяем полное совпадение
    if cityName in citySet:
        return True

    # Разбиваем по пробелу и проверяем каждую часть
    for part in cityName.split(" "):
        if part in citySet:
            return True

    # Разбиваем по дефису и проверяем каждую часть
    for part in cityName.split("-"):
        if part in citySet:
            return True

    return False

