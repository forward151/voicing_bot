from telegram.ext import Updater, MessageHandler, Filters, ChatMemberHandler
from translating import translate_text


def reply(update, context):
    if update.channel_post.caption is None and update.channel_post.text is not None:
        answer = translate_text(update.channel_post.text)
        update.channel_post.reply_text(f'Транслированное сообщение: "{answer}"')
    elif update.channel_post.caption is not None and update.channel_post.text is None:
        answer = translate_text(update.channel_post.caption)
        update.channel_post.reply_text(f'Транслированное сообщение: "{answer}"')
    # update.message.edit_text(text='asdsasdsasd')


def main():
    updater = Updater('TOKEN')
    dp = updater.dispatcher
    text_handler = MessageHandler((Filters.text | Filters.photo), reply)
    dp.add_handler(text_handler)
    updater.start_polling()



if __name__ == '__main__':
    main()
