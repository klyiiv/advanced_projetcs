def ugadai_gorod(city):
    import os
    import sys
    import random
    import requests
    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

    SCREEN_SIZE = [600, 530]

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

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": city,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)


    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    a = toponym_coodrinates.split()

    class Example(QWidget):
        def __init__(self):
            super().__init__()
            self.c = 0
            self.sp = ["0.005,0.005", "0.009,0.009", "0.0008,0.0008", "0.0075,0.0075", "0.0089,0.0089", "0.00005,0.00005", "0.0000001,0.0000001"]
            self.coordinates = [a]
            self.getImage(self.coordinates[self.c])
            self.initUI()

            self.btn = QPushButton('-->', self)
            self.btn.resize(100, 30)
            self.btn.move(300, 480)
            self.btn.clicked.connect(self.do)

            self.btn1 = QPushButton('<--', self)
            self.btn1.resize(100, 30)
            self.btn1.move(150, 480)
            self.btn1.clicked.connect(self.do1)

            self.label = QLabel("", self)
            self.label.move(450, 480)
            self.label.resize(100, 30)

        def do(self):

            self.c = (self.c + 1) % len(self.sp)
            self.getImage(self.coordinates[0])
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.update()

        def do1(self):

            self.c = (self.c - 1) % len(self.sp)
            self.getImage(self.coordinates[0])
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.update()

        def getImage(self, coords):
            # &spn={self.sp[self.c]}
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}8&spn={self.sp[self.c]}&l={random.choice(['sat', 'map'])}"
            response = requests.get(map_request)


            # Запишем полученное изображение в файл.
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)

        def initUI(self):
            self.setGeometry(100, 100, *SCREEN_SIZE)
            self.setWindowTitle('Угадай город')

            ## Изображение
            self.pixmap = QPixmap(self.map_file)
            self.image = QLabel(self)
            self.image.move(0, 0)
            self.image.resize(600, 450)
            self.image.setPixmap(self.pixmap)

        def closeEvent(self, event):
            """При закрытии формы подчищаем за собой"""
            os.remove(self.map_file)

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec())

# примеры вызова
# ugadai_gorod("Нью-Йорк")
# ugadai_gorod("Москва")
# ugadai_gorod("Смоленск")
