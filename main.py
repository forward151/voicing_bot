import telegram
from telegram.ext import Updater, MessageHandler, Filters
from translating import translate_text
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import dotenv_values
import os
from datetime import datetime
from token_generate import generate_token


def is_caption_or_text(caption, text):
    if not caption and text:  # если есть текст но нет подписи (без картинки)
        return text  # выводим текст
    elif not text and caption:  # если есть подпись, но нет текста (есть картинка)
        return caption  # выводим подпись
    else:
        return False  # иначе выводим, что ничего нет


def create_token(filename):
    keys = dotenv_values('.env')
    folder_id = keys['FOLDER_ID']  # достаем folder_id
    with open(filename, 'r') as file:  # читаем файл с iam token
        text = file.read().split('\n')
    dt = text[1]  # берем время из файла
    old_time = datetime.strptime(dt, "%d.%m.%Y %H:%M")  # смотрим его
    new_time = datetime.now()  # берем текущее время
    if (new_time - old_time).seconds > 3600:  # если разница больше часа
        iam_token = generate_token()  # генерируем новый токен
        text[0] = iam_token  # заменяем старый токен
        text[1] = f'{new_time.day}.{new_time.month}.{new_time.year} {new_time.hour}:{new_time.minute}'  # заменяем старое время
        with open(filename, 'w') as file:  # записываем в файл
            file.write('\n'.join(text))
        return iam_token, folder_id  # выводим token и folder_id
    else:
        iam_token = text[0]  # иначе берем старый token
        return iam_token, folder_id  # выводим


def reply(update, context):
    upd_ch_post = update.channel_post  # создаем переменную поста
    if upd_ch_post is None:  # Если сообщение пришло из чата, то ничего не делаем
        return
    caption = upd_ch_post.caption  # читаем подпись и текст
    text = upd_ch_post.text

    result = is_caption_or_text(caption, text)  # смотрим результат
    iam_token, folder_id = create_token('iam_token.txt')  # генерируем token и folder_id
    engine = 'yandex'  # выбираем движок

    if result:  # если в результате что-то есть
        filename = translate_text(result, engine, iam_token, folder_id)  # создаем файлс озвучкой и возвращаем имя
        with open(filename, 'rb') as file:  # открываем файл
            upd_ch_post.reply_text('.', reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='hello', callback_data=file)]]))  # отсылаем голос
        os.remove(filename)  # удаляем файл, чтобы не засорять память


def main():
    print('Start initialization...')
    try:
        keys = dotenv_values('.env')  # открываем файл env
        telegram_token = keys['TELEGRAM_TOKEN']  # берем телеграммовский токен
        print('Token found')
        updater = Updater(telegram_token)  # подключаем updater
        print('Token is correct')
        dp = updater.dispatcher  # связываем с диспетчером
        text_handler = MessageHandler((Filters.text | Filters.photo), reply)  # объявляем вызов по сообщению
        dp.add_handler(text_handler)  # добавляем вызов
        print('Initialization completed successfully')
        print('Start working')
        updater.start_polling()  # начинаем опрос
    except KeyError:  # если нет env файла или там нет ключа
        print('Error in .env file')
    except telegram.error.InvalidToken:  # если ключ неверный
        print('Token is invalid')


if __name__ == '__main__':
    # todo: graceful shutdown
    main()  # запуск
