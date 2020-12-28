from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import my_logging, os

logger = my_logging.get_logger(__name__)

dict_users = {}
stat_users = {}


if os.access('file_users.txt', os.F_OK):
    with open('file_users.txt',) as inp:
        for i in inp.readlines():
            key,val = i.strip().split(':')
            dict_users[key] = val
else:
    open('file_users.txt', 'w')

if os.access('stat_users.txt', os.F_OK):
    with open('stat_users.txt',) as inp:
        for i in inp.readlines():
            key,val = i.strip().split(':')
            stat_users[key] = val
else:
    open('stat_users.txt', 'w')



def statistic_updata (update):
    user = update.message.chat.username
    user_id = str(update.message.chat.id)
    text = update.message.text

    logger.debug(f'Пользователь {user}, '
                 f'chat_id = {user_id}, '
                 f'Выполнена функция - stat, '
                 f'текст_сообщения = {text}')

    if user_id not in dict_users:
        dict_users[user_id] = user
        with open('file_users.txt', 'a') as out:
            out.write('{}:{}\n'.format(user_id, user))

    if user_id not in stat_users:
        quantity_messages = 1
        stat_users[user_id] = quantity_messages
    else:
        quantity_messages = int(stat_users[user_id])
        quantity_messages += 1
        stat_users[user_id] = quantity_messages


    with open('stat_users.txt', 'w') as out:
        for key, val in stat_users.items():
            out.write('{}:{}\n'.format(key, val))



def inline_statistic_updata (update):
    inline_user = update.inline_query.from_user.username
    inline_user_id = str(update.inline_query.from_user.id)

    if inline_user_id not in dict_users:
        dict_users[inline_user_id] = inline_user
        with open('file_users.txt', 'a') as out:
            out.write('{}:{}\n'.format(inline_user_id, inline_user))

    if inline_user_id not in stat_users:
        quantity_messages = 1
        stat_users[inline_user_id] = quantity_messages
    else:
        quantity_messages = int(stat_users[inline_user_id])
        quantity_messages += 1
        stat_users[inline_user_id] = quantity_messages

    with open('stat_users.txt', 'w') as out:
        for key, val in stat_users.items():
            out.write('{}:{}\n'.format(key, val))



def stat (update, context):
    statistic_updata(update)
    lens_user = []
    for k in dict_users:
        lens_user += f'{k} : {dict_users[k]}, Количество запросов {stat_users[k]}\n'
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f'Количество уникальных пользователей: {len(dict_users)}\n'
                                               f"{''.join(lens_user)}")


