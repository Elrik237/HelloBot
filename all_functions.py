import telegram
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import logging, datetime,os

if os.environ.get('token_bot'):
    print('Погнали!')
else:
    print('Нужен token_bot. Добавь его или не буду работать!')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG, filename='myapp.log')
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот и только начинаю "
                                                                    "развиваться. В будущем я захвачу "
                                                                    "человечество!!!")

time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

def echo(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)

def time_now(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=time)

def inline_time_now(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=1,
            title='Time now',
            input_message_content=InputTextMessageContent('Текущая дата и время: ' + time)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")







