import datetime
import logging
import os
import os.path

import pytz
from chatbase import Message

import requests


class Statistic:
    def __init__(self):
        self.token_bd = os.environ['token_bd']
        self.url_bd = "http://89.223.90.206:8000/click_statistics/"

    def statistic_updata(self, user_id, user_name, user_fullname, f):
        time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m/%d/%Y %H:%M')
        logging.debug(f'Пользователь {user_name}, '
                      f'chat_id = {user_id}, '
                      f'Выполнена функция - {f}')

        msg = Message(api_key=os.environ['token_chatbase'],  # TODO Добавить в конструктор
                      platform="Telegram",
                      version="0.2",
                      user_id=f"{user_id}",
                      intent=f"{f}")
        msg.send()

        if user_name is None:
            data = {'time': time, 'f_name': f, 'user_id': user_id, 'user_name': 'None',
                    'user_fullname': user_fullname}
            requests.post(self.url_bd, data=data, headers={'Authorization': 'Token {}'.format(self.token_bd)})
        else:
            data = {'time': time, 'f_name': f, 'user_id': user_id, 'user_name': user_name,
                    'user_fullname': user_fullname}
            requests.post(self.url_bd, data=data, headers={'Authorization': 'Token {}'.format(self.token_bd)})

    def inline_statistic_updata(self, inline_user_id, inline_user_name, inline_user_fullname, query, f):
        time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m/%d/%Y %H:%M')
        logging.debug(f'Пользователь {inline_user_name}, '
                      f'chat_id = {inline_user_id}, '
                      f'Выполнена функция - {f}, '
                      f'текст_сообщения = {query}')

        msg = Message(api_key=os.environ['token_chatbase'],
                      platform="Telegram",
                      version="0.1",
                      user_id=f"{inline_user_id}",
                      message=f"{query}",
                      intent=f"{f}")
        msg.send()

        if inline_user_name is None:
            data = {'time': time, 'f_name': f, 'user_id': inline_user_id,
                    'user_name': 'None', 'user_fullname': inline_user_fullname}
            requests.post(self.url_bd, data=data, headers={'Authorization': 'Token {}'.format(self.token_bd)})
        else:
            data = {'time': time, 'f_name': f, 'user_id': inline_user_id,
                    'user_name': inline_user_name, 'user_fullname': inline_user_fullname}
            requests.post(self.url_bd, data=data, headers={'Authorization': 'Token {}'.format(self.token_bd)})

    def stat(self):

        response = requests.get(self.url_bd, headers={"Authorization": "Token {}".format(self.token_bd)})
        data = response.json()
        users = {}
        list = []

        for i in data:
            user_id = i['user_id']
            if user_id not in users:
                users[user_id] = [i['user_fullname'], i['user_name'], 1]
            else:
                count = users[i["user_id"]][2]
                count += 1
                users[user_id] = [i['user_fullname'], i['user_name'], count]

        count_user = len(users)
        list += f'Количество уникальных пользователей: {count_user}\n\n'

        for id in users.keys():
            if users[id][0] is None:
                list += f'{id} : {users[id][0]},\n ' \
                        f'Количество запросов {users[id][2]}\n\n'
            else:
                list += f"{id} : {users[id][0]}, (@{users[id][1]})\n " \
                        f'Количество запросов {users[id][2]}\n\n'

        return list
