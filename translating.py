from google_translating import google_translating
from yandex_translating import yandex_translating
import uuid


def translate_text(text, engine, iam_token, folder_id):
    code = uuid.uuid4()  # создаем уникальное название файла
    filename = f'{code}.ogg'  # создаем имя файла
    if engine == 'google':  # если движок гугла
        google_translating(text, filename)  # вызываем его
    elif engine == 'yandex':  # если движок яндекса
        yandex_translating(text, filename, iam_token, folder_id)  # вызываем его
    return filename  # возвращаем имя файла
