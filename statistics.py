import os.path
import my_logging
import json
from chatbase import Message


class Statistic:
    logger = my_logging.get_logger(__name__)

    dict_users = {}
    stat_users = {}

    if os.path.exists('file_users.json'):
        with open('file_users.json', 'r') as inp:
            dict_users = json.load(inp)
    else:
        with open('file_users.json', 'w') as out:
            json.dump(dict_users, out)

    if os.path.exists('stat_users.json'):
        with open('stat_users.json', 'r') as inp:
            stat_users = json.load(inp)
    else:
        with open('stat_users.json', 'w') as out:
            json.dump(stat_users, out)

    def chatbase(self, update, f):
        user_id = str(update.message.chat.id)
        text = update.message.text

        msg = Message(api_key=os.environ['token_chatbase'],
                      platform="Telegram",
                      version="0.1",
                      user_id=f"{user_id}",
                      message=f"{text}",
                      intent=f"{f}")
        msg.send()

    def statistic_updata(self, update):
        user = update.message.chat.username
        user_id = str(update.message.chat.id)
        text = update.message.text

        Statistic.logger.debug(f'Пользователь {user}, '
                               f'chat_id = {user_id}, '
                               f'Выполнена функция - stat, '
                               f'текст_сообщения = {text}')

        if user_id not in Statistic.dict_users:
            Statistic.dict_users[user_id] = user
        with open('file_users.json', 'w') as out:
            json.dump(Statistic.dict_users, out)

        if user_id not in Statistic.stat_users:
            quantity_messages = 1
            Statistic.stat_users[user_id] = quantity_messages
        else:
            quantity_messages = int(Statistic.stat_users[user_id])
            quantity_messages += 1
            Statistic.stat_users[user_id] = quantity_messages

        with open('stat_users.json', 'w') as out:
            json.dump(Statistic.stat_users, out)

    def inline_statistic_updata(self, update):
        inline_user = update.inline_query.from_user.username
        inline_user_id = str(update.inline_query.from_user.id)

        if inline_user_id not in Statistic.dict_users:
            Statistic.dict_users[inline_user_id] = inline_user
            with open('file_users.json', 'a') as out:
                json.dump(Statistic.dict_users, out)

        if inline_user_id not in stat_users:
            quantity_messages = 1
            Statistic.stat_users[inline_user_id] = quantity_messages
        else:
            quantity_messages = int(stat_users[inline_user_id])
            quantity_messages += 1
            Statistic.stat_users[inline_user_id] = quantity_messages

        with open('stat_users.json', 'w') as out:
            json.dump(Statistic.stat_users, out)

    def stat(self, update, context):
        f = 'stat'
        Statistic().statistic_updata(update)
        Statistic().chatbase(update, f)
        lens_user = []
        for k in Statistic.dict_users:
            lens_user += f'{k} : {Statistic.dict_users[k]}, Количество запросов {Statistic.stat_users[k]}\n'
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'Количество уникальных пользователей: {len(Statistic.dict_users)}\n'
                                                   f"{''.join(lens_user)}")
