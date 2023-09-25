import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
import math
# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

a = input("Введите адрес ")

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"


def get_distance(*p1):
    # p1 и p2 - это кортежи из двух элементов - координаты точек
    radius = 6373.0

    ans = 0
    for i in range(len(p1)):
        lon1 = math.radians(p1[0][i][0])
        lat1 = math.radians(p1[0][i][1])
        lon2 = math.radians(p1[0][i + 1][0])
        lat2 = math.radians(p1[0][i + 1][1])

        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)

        distance = radius * c
        ans += distance

    return ans


geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": a,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

address_ll = f"{toponym_longitude},{toponym_lattitude}"

geocoder_params1 = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_coodrinates,
    "kind": "district",
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params1)
if not response:
    # ...
    pass
# Преобразуем ответ в json-объект

json_response = response.json()

print(json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'])
