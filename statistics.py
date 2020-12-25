from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import my_logging

logger = my_logging.get_logger(__name__)
dict_users = {'139664903' : 'Petya',}

def collection_id(update):
    user = update.message.chat.username
    user_id = update.message.chat.id
    if user_id not in dict_users:
        dict_users[user_id] = user


def inline_collection_id(update):
    inline_user = update.inline_query.from_user.username
    inline_user_id = update.inline_query.from_user.id
    if inline_user_id not in dict_users:
        dict_users[inline_user_id] = inline_user


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