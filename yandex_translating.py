import requests


def synthesis(folder_id, iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'  # url для запроса
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'zahar',
        'folderId': folder_id,
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:  # открываем ответ
        if resp.status_code != 200:  # если ошибка возникла
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):  # если ее нет то возвращаем чанк не храня его в памяти
            yield chunk


def yandex_translating(text, filename, iam_token, folder_id):
    with open(filename, "wb") as f:  # открываем переданный файл
        for audio_content in synthesis(folder_id, iam_token, text):  # для каждого чанка
            f.write(audio_content)  # записываем
