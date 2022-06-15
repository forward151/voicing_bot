from telegram.ext import Updater, MessageHandler, Filters, ChatMemberHandler
from translating import translate_text
from dotenv import dotenv_values
import os

def is_text(caption, text):
    if not caption and text:
        return text
    else:
        return False

def is_caption(caption, text):
    if caption and not text:
        return caption
    else:
        return False

def reply_answer(text, update):
    translate_text(text)
    update.channel_post.reply_audio(open('./voice.ogg', 'rb'))
    os.remove('./voice.ogg')


def reply(update, context):
    caption = update.channel_post.caption
    text = update.channel_post.text
    if is_caption(caption, text):
        reply_answer(caption, update)
    elif is_text(caption, text):
        reply_answer(text, update)


def main():
    keys = dotenv_values('.env')
    updater = Updater(keys['TELEGRAM_KEY'])
    dp = updater.dispatcher
    text_handler = MessageHandler((Filters.text | Filters.photo), reply)
    dp.add_handler(text_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()