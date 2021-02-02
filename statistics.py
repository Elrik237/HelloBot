import datetime
import logging
import os
import os.path

from chatbase import Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.clickstatistics import DeclarativeBase, ClickStatistics


class Statistic:
    def __init__(self):
        self.engine = create_engine('sqlite:///click_statistics.db', echo=None)

        DeclarativeBase.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def statistic_updata(self, user_id, user_name, user_fullname, f):
        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
        logging.debug(f'Пользователь {user_name}, '
                      f'chat_id = {user_id}, '
                      f'Выполнена функция - {f}')

        msg = Message(api_key=os.environ['token_chatbase'],  # TODO Добавить в конструктор
                      platform="Telegram",
                      version="0.2",
                      user_id=f"{user_id}",
                      intent=f"{f}")
        msg.send()

        click_statistics = ClickStatistics(time, f, user_id, user_name, user_fullname)
        self.session.add(click_statistics)
        self.session.commit()
        self.session.close()

    def inline_statistic_updata(self, inline_user_id, inline_user_name, inline_user_fullname, query, f):
        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
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

        click_statistics = ClickStatistics(time, f, inline_user_id, inline_user_name, inline_user_fullname)
        self.session.add(click_statistics)
        self.session.commit()
        self.session.close()

    def stat(self):

        list = []
        count_user = self.session.query(ClickStatistics.user_id).group_by(ClickStatistics.user_id).count()
        list += f'Количество уникальных пользователей: {count_user}\n\n'

        for user_id in self.session.query(ClickStatistics.user_id).distinct():
            count_query = self.session.query(ClickStatistics). \
                filter(ClickStatistics.user_id == user_id.user_id).count()
            user_name = self.session.query(ClickStatistics.user_name).filter(
                ClickStatistics.user_id == user_id.user_id).first()
            user_fullname = self.session.query(ClickStatistics.user_fullname).filter(
                ClickStatistics.user_id == user_id.user_id).first()

            if user_name.user_name == None:
                list += f'{user_id.user_id} : {user_fullname.user_fullname},\n ' \
                        f'Количество запросов {count_query}\n\n'
            else:
                list += f'{user_id.user_id} : {user_fullname.user_fullname} (@{user_name.user_name}),\n ' \
                        f'Количество запросов {count_query}\n\n'
        return list
