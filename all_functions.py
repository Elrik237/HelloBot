from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import os
import datetime
import my_logging
from statistics import Statistic

logger = my_logging.get_logger(__name__)

if os.environ.get('token_bot'):
    logger.info('Погнали!')
else:
    logger.info('Нужен token_bot. Добавь его или не буду работать!')


def start(update, context):
    f = 'start'
    Statistic().statistic_updata(update, f)
    text = "%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n" % ("Привет, я бот который только начинает развиваться!",
                                                              "Если не использовать команды ниже, "
                                                              "я буду просто повторять Ваше сообщение(",
                                                              "",
                                                              "Команда /time_now покажет текущуюю дату и время.",
                                                              "Команда /caps вернет Ваше сообщенем капсом.",
                                                              "",
                                                              "Еще есть команда, которая покажет статистику "
                                                              "по этому боту, но я Вам не скажу)",
                                                              "",
                                                              "По вопросам пишите @Elrik237")
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')


def echo(update, context):
    f = 'echo'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)


def time_now(update, context):
    f = 'time_now'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=time)


def inline_time_now(update, context):
    f = 'inlin_time_now'
    Statistic().inline_statistic_updata(update, f)
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
    f = 'caps'
    Statistic().statistic_updata(update, f)
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update, context):
    f = 'unknown'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
