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

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz",
    "results": 10
}

response = requests.get(search_api_server, params=search_params)
if not response:
    # ...
    pass
# Преобразуем ответ в json-объект

m = []
d = []
json_response = response.json()
for i in range(len(json_response)):
    # Получаем первую найденную организацию.
    organization = json_response["features"][i]
    # Название организации.
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]

    # Получаем координаты ответа.
    point = organization["geometry"]["coordinates"]

    org_point = "{0},{1}".format(point[0], point[1])
    m.append(org_point)
    d.append(organization["properties"]["CompanyMetaData"]["Hours"]["text"].split())
    # delta = "0.005"
s = ""
for i in m:
    if d[m.index(i)][0] == 'ежедневно,':
        s += i + ",pm2dgl~"
    elif "-" in d[m.index(i)][0]:
        s += i + ",pm2rdl~"
    else:
        s += i + ",pm2grl~"
s = s[:-1]
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    # "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": s
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
print("***Красная метка - введённый адрес, зелёные - ближайшие аптеки")
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()

