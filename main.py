import telegram
from telegram.ext import Updater
from telegram.ext import InlineQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import datetime
import os

if os.environ.get('token_bot'):
    print('Погнали!')
else:
    print('Нужен token_bot. Добавь его или не буду работать!')


bot = telegram.Bot(token=os.environ['token_bot'])


updater = Updater(token=os.environ['token_bot'], use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот и только начинаю "
                                                                    "развиваться. В будущем я захвачу "
                                                                    "человечество!!!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')

def echo(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def time_now(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=time)

time_now_handler = CommandHandler('time_now', time_now)
dispatcher.add_handler(time_now_handler)


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

inline_time_now_handler = InlineQueryHandler(inline_time_now)
dispatcher.add_handler(inline_time_now_handler)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()
updater.idle()


