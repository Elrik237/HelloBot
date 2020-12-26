from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import my_logging

logger = my_logging.get_logger(__name__)

dict_users = {}

with open('file_users.txt') as inp:
    for i in inp.readlines():
        key,val = i.strip().split(':')
        dict_users[key] = val




def collection_id(update):
    user = update.message.chat.username
    user_id = str(update.message.chat.id)
    if user_id not in dict_users:
        dict_users[user_id] = user
        with open('file_users.txt', 'a') as out:
            for key, val in dict_users.items():
                out.write('{}:{}\n'.format(key, val))

def inline_collection_id(update):
    inline_user = update.inline_query.from_user.username
    inline_user_id = str(update.inline_query.from_user.id)
    if inline_user_id not in dict_users:
        dict_users[inline_user_id] = inline_user
        with open('file_users.txt', 'a') as out:
            for key, val in dict_users.items():
                out.write('{}:{}\n'.format(key, val))


def stat (update, context):
    collection_id(update)
    logger.debug(f'Пользователь {update.message.chat.username}, '
                 f'chat_id = {update.message.chat.id}, '
                 f'Выполнена функция - stat, '
                 f'текст_сообщения = {update.message.text}')
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Количество уникальных пользователей: {len(dict_users)}')
    for k in dict_users:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'{k} : {dict_users[k]}')