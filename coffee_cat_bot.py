import pytz
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, \
    MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import requests
import os
import datetime

from statistics import Statistic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user_requests import DeclarativeBase, UserRequests


class CoffeeCatBot:
    def __init__(self):
        self.stat = Statistic()
        self.updater = Updater(token=os.environ['token_bot'], use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('time_now', self.time_now))
        dp.add_handler(CommandHandler('stat', self.statistic))
        dp.add_handler(CommandHandler("cat", self.send_cat))
        dp.add_handler(CommandHandler("coffee", self.coffee))
        dp.add_handler(CallbackQueryHandler(self.get_callback_from_button))
        dp.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))
        dp.add_handler(MessageHandler(Filters.command, self.unknown))
        dp.add_handler(InlineQueryHandler(self.inline_))

        self.logger = logging.getLogger(__name__)

        if os.environ.get('token_bot'):
            self.logger.info('Погнали!')
        else:
            self.logger.info('Нужен token_bot. Добавь его или не буду работать!')

        self.updater.start_polling()

        self.engine = create_engine('sqlite:///user_requests.db', echo=None)

        DeclarativeBase.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.query_user_id = []
        self.date = []

    def start(self, update, context):
        f = 'start'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        text = "%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n" % (
            "Привет, я бот который только начинает развиваться!",
            "Если не использовать команды ниже, "
            "я буду просто повторять Ваше сообщение(",
            "",
            "Команда /time_now покажет текущуюю дату и время.",
            "Команда /cat покажет вам картунку с котиком.",
            "",
            "Еще есть команда, которая покажет статистику "
            "по этому боту, но я Вам не скажу)",
            "",
            "",
            "По вопросам пишите @Elrik237",
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        keyboard1 = [
            [
                InlineKeyboardButton("Текущая дата и время", callback_data='1'),
                InlineKeyboardButton("Картинки с котиками", callback_data='2'),
            ],
            [
                InlineKeyboardButton("Выпить кофе с @Elrik237", callback_data='3')
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard1)

        update.message.reply_text('Пожалуйста выберите:', reply_markup=reply_markup)

    def get_cat(self):
        try:
            r = requests.get('http://thecatapi.com/api/images/get?format=src')
            url = r.url
        except:
            url = self.get_cat()
            logging.info('Проблемы с парсингом')
            pass
        return url

    def send_cat(self, update, context):
        f = 'cat'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)

        context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=self.get_cat(),
                              reply_markup=self.draw_button())

    def draw_button(self):
        keys = [[InlineKeyboardButton('🐈Еще котика?!🐈', callback_data='2')]]
        return InlineKeyboardMarkup(inline_keyboard=keys)

    def coffee(self, update, context):
        f = 'coffee'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        keyboard = [
            [
                InlineKeyboardButton("Сегодня", callback_data='4'),
                InlineKeyboardButton("Завтра", callback_data='5'),
            ],
            [
                InlineKeyboardButton("На выходных", callback_data='6')
            ],
        ]

        markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Когда вы хотите пригласить @Elrik237 на кофе?',
                                 reply_markup=markup)

    def get_callback_from_button(self, update, context):

        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        query = update.callback_query

        keyboard2 = [
            [
                InlineKeyboardButton("Да", callback_data='7'),
                InlineKeyboardButton("Нет", callback_data='8'),
            ],
            [],
        ]

        markup1 = InlineKeyboardMarkup(keyboard2, one_time_keyboard=True)

        def chat(day):
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Я сообщил @Elrik237, что вы хотите {day} встретиться!')
            context.bot.send_message(chat_id=139664901,
                                     text=f'{user_fullname} : @{user_name} хочет {day} выпить с вами кофе!',
                                     reply_markup=markup1)
            self.query_user_id.insert(0, user_id)

        if int(query.data) == 2:
            self.send_cat(update, context)
        elif int(query.data) == 1:
            self.time_now(update, context)
        elif int(query.data) == 3:
            self.coffee(update, context)
        elif int(query.data) == 4:
            chat('сегодня')
            date_today = datetime.datetime.now().strftime('%d/%m/%Y')
            self.date.clear()
            self.date.append(date_today)

        elif int(query.data) == 5:
            chat('завтра')
            date_now = datetime.datetime.now()
            duration_minutes = datetime.timedelta(days=1)
            result = date_now + duration_minutes
            date_tomorrow = result.strftime('%d/%m/%Y')
            self.date.clear()
            self.date.append(date_tomorrow)

        elif int(query.data) == 6:
            chat('на выходных')
            data = datetime.datetime.today().weekday()
            data_week = 5 - data
            date_now = datetime.datetime.now()
            duration_minutes = datetime.timedelta(days=data_week)
            result = date_now + duration_minutes
            duration_minutes_1 = datetime.timedelta(days=1)
            result_1 = result + duration_minutes_1
            date_weekday_2 = result_1.strftime('%d/%m/%Y')
            date_weekday = result.strftime('%d/%m/%Y')
            self.date.clear()
            self.date.append(f'{date_weekday} - {date_weekday_2}')

        elif int(query.data) == 7:
            context.bot.send_message(chat_id=self.query_user_id[0],
                                     text='@Elrik237 готов с Вами встретиться!')
            context.bot.send_message(chat_id=139664901, text='Я отправил ваш ответ')

            user_requests = UserRequests(user_id, user_name, user_fullname, self.date[0])
            self.session.add(user_requests)
            self.session.commit()
            self.session.close()

        elif int(query.data) == 8:
            context.bot.send_message(chat_id=self.query_user_id[0],
                                     text='@Elrik237 не готов с Вами встретиться! Давайте запланируем другой день!')
            context.bot.send_message(chat_id=139664901, text='Я отправил ваш ответ')

    def echo(self, update, context):
        f = 'echo'
        time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        if user_id == 139664901 and update.message.text == '?':
            self.nearest_event(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)

    def time_now(self, update, context):
        f = 'time_now'
        time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m/%d/%Y %H:%M')

        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)

        context.bot.send_message(chat_id=update.effective_chat.id, text=time)

    def inline_(self, update, context):
        f = 'inlin_'
        time = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime('%m/%d/%Y %H:%M')
        query = update.inline_query.query
        inline_user_fullname = f'{update.inline_query.from_user.first_name} {update.inline_query.from_user.last_name}'
        inline_user_name = update.inline_query.from_user.username
        inline_user_id = str(update.inline_query.from_user.id)
        self.stat.inline_statistic_updata(inline_user_id, inline_user_name, inline_user_fullname, query, f)

        results = list()
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='Дата и время',
                description='Выводит текущую дату и врумя',
                input_message_content=InputTextMessageContent('Текущая дата и время: ' + time)
            )
        )

        context.bot.answer_inline_query(update.inline_query.id, results=results)

    def nearest_event(self, update, context):
        f = 'nearest_event'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        date_today = datetime.datetime.now().strftime('%d/%m/%Y')
        q = self.session.query(UserRequests).filter(UserRequests.data == date_today). \
            group_by(UserRequests.user_id)
        if not q.first():
            context.bot.send_message(chat_id=139664901, text=f'У Вас на сегодня ничего не запланированно')

        else:
            for nearest_event in q:
                context.bot.send_message(chat_id=139664901, text=f'У Вас на сегодня '
                                                                 f'запланирована встреча с {nearest_event.user_fullname}')

    def statistic(self, update, context):
        f = 'stat'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        q = self.stat.stat()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{''.join(q)}\n"
                 f"Также статистика ведется на chatbase.com, для ознакомления с ней обратитесь к @Elrik237"
        )

    def unknown(self, update, context):
        f = 'unknown'
        user_fullname = f'{update.effective_user.first_name} {update.effective_user.last_name}'
        user_name = update.effective_user.username
        user_id = update.effective_user.id
        self.stat.statistic_updata(user_id, user_name, user_fullname, f)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I didn't understand that command.")
