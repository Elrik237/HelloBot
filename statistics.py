import os.path
import my_logging
from chatbase import Message
import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///click_statistics.db', echo=None)

Base = declarative_base()


class Click_statistics(Base):
    __tablename__ = 'click_statistics'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    f_name = Column(String)
    user_id = Column(String)
    username = Column(String)
    user_name = Column(String)

    def __init__(self, data, f_name, user_id, username, user_name):
        self.data = data
        self.f_name = f_name
        self.user_id = user_id
        self.username = username
        self.user_name = user_name

    def __repr__(self):
        return "<User('%s','%s', '%s', '%s', '%s')>" % (
            self.data, self.f_name, self.user_id, self.username, self.user_name)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Statistic:
    logger = my_logging.get_logger(__name__)

    def statistic_updata(self, update, f):
        user_name = f'{update.effective_user.first_name} {update.effective_user.last_name}'
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

        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

        click_statistics = Click_statistics(time, f, user_id, user, user_name)
        session.add(click_statistics)
        session.commit()

    def inline_statistic_updata(self, update, f):
        inline_user_name = f'{update.inline_query.from_user.first_name} {update.inline_query.from_user.last_name}'
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

        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

        click_statistics = Click_statistics(time, f, inline_user_id, inline_user, inline_user_name)
        session.add(click_statistics)
        session.commit()

    def stat(self, update, context):
        f = 'stat'
        Statistic().statistic_updata(update, f)

        lens_user = {}
        list_ = []

        for q in session.query(Click_statistics.user_id):
            c = session.query(Click_statistics.user_id).filter(Click_statistics.user_id == q[0]).count()
            for u_n in session.query(Click_statistics.user_name).filter(Click_statistics.user_id == q[0]):
                for n in session.query(Click_statistics.username).filter(Click_statistics.user_id == q[0]):
                    if q[0] not in lens_user:
                        lens_user[q[0]] = [u_n[0], n[0], c]
                    else:
                        lens_user[q[0]] = [u_n[0], n[0], c]

        for k in lens_user:
            if lens_user[k][1] == None:
                list_ += f'{k} : {lens_user[k][0]},\n Количество запросов {lens_user[k][2]}\n\n'
            else:
                list_ += f'{k} : {lens_user[k][0]} (@{lens_user[k][1]}),\n Количество запросов {lens_user[k][2]}\n\n'

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Количество уникальных пользователей: {len(lens_user)}\n\n'
                 f"{''.join(list_)}\n"
                 f"Также статистика ведется на chatbase.com, для ознакомления с ней обратитесь к @Elrik237"
        )
