import os.path
import my_logging
import json
from chatbase import Message
import datetime

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///click_statistics.db', echo=True)

Base = declarative_base()


class Click_statistics(Base):
    __tablename__ = 'click_statistics'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    f_name = Column(String)
    user_id = Column(Integer)

    def __init__(self, data, f_name, user_id):
        self.data = data
        self.f_name = f_name
        self.user_id = user_id

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.data, self.f_name, self.user_id)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



class Datebase:
    dict_users = {}

    if os.path.exists('file_users.json'):
        with open('file_users.json', 'r') as inp:
            dict_users = json.load(inp)
    else:
        with open('file_users.json', 'w') as out:
            json.dump(dict_users, out)


class Statistic:
    logger = my_logging.get_logger(__name__)

    def statistic_updata(self, update, f):
        user = update.effective_user.username
        user_id = str(update.effective_user.id)
        Statistic.logger.debug(f'Пользователь {user}, '
                               f'chat_id = {user_id}, '
                               f'Выполнена функция - {f}')

        msg = Message(api_key=os.environ['token_chatbase'],
                      platform="Telegram",
                      version="0.2",
                      user_id=f"{user_id}",
                      intent=f"{f}")
        msg.send()

        if user_id not in Datebase.dict_users:
            Datebase.dict_users[user_id] = [user, 1]
        else:
            quantity_messages = Datebase.dict_users[user_id][1]
            quantity_messages += 1
            Datebase.dict_users[user_id] = [user, quantity_messages]

        with open('file_users.json', 'w') as out:
            json.dump(Datebase.dict_users, out)

        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

        click_statistics = Click_statistics(time, f, user_id)
        session.add(click_statistics)
        session.commit()

    def inline_statistic_updata(self, update, f):
        inline_user = update.inline_query.from_user.username
        inline_user_id = str(update.inline_query.from_user.id)
        query = update.inline_query.query
        Statistic.logger.debug(f'Пользователь {inline_user}, '
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

        if inline_user_id not in Datebase.dict_users:
            Datebase.dict_users[inline_user_id] = [inline_user, 1]
        else:
            quantity_messages = Datebase.dict_users[inline_user_id][1]
            quantity_messages += 1
            Datebase.dict_users[inline_user_id] = [inline_user, quantity_messages]

        with open('file_users.json', 'w') as out:
            json.dump(Datebase.dict_users, out)

        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

        click_statistics = Click_statistics(time, f, inline_user_id)
        session.add(click_statistics)
        session.commit()

    def stat(self, update, context):
        f = 'stat'
        Statistic().statistic_updata(update, f)
        lens_user = []
        for k in Datebase.dict_users:
            lens_user += f'{k} : {Datebase.dict_users[k][0]}, Количество запросов {Datebase.dict_users[k][1]}\n'
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Количество уникальных пользователей: {len(Datebase.dict_users)}\n'
                 f"{''.join(lens_user)}\n"
                 f"Также статистика ведется на chatbase.com, для ознакомления с ней обратитесь к @Elrik237"
        )
        with open('click_statistics.db', 'rb') as doc:
            context.bot.sendDocument(chat_id=update.effective_chat.id, document=doc)
