from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler, MessageHandler, Filters
import datetime, os
import my_logging

logger = my_logging.get_logger(__name__)



if os.environ.get('token_bot'):
    logger.info('Погнали!')
else:
    logger.info('Нужен token_bot. Добавь его или не буду работать!')




def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот и только начинаю "
                                                                    "развиваться. В будущем я захвачу "
                                                                    "человечество!!!")



time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')


def echo(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    logger.debug(f'Пользователь {update.message.chat.username}, '
                 f'chat_id = {update.message.chat.id}, '
                 f'Выполнена функция - echo, '
                 f'текст_сообщения = {update.message.text}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)


def time_now(update, context):
    logger.debug(f'Пользователь {update.message.chat.username}, '
                 f'chat_id = {update.message.chat.id}, '
                 f'Выполнена функция - time_now, '
                 f'текст_сообщения = {update.message.text}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=time)


def inline_time_now(update, context):
    query = update.inline_query.query
    logger.debug(f'Пользователь {update.inline_query.from_user.username}, '
                 f'chat_id = {update.inline_query.from_user.id}, '
                 f'Выполнена функция - inlin_time_now, '
                 f'текст_сообщения = {update.inline_query.query}')
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
    logger.debug(f'Пользователь {update.message.chat.username}, '
                 f'chat_id = {update.message.chat.id}, '
                 f'Выполнена функция - caps, '
                 f'текст_сообщения = {update.message.text}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update, context):
    logger.debug(f'Пользователь {update.message.chat.username}, '
                 f'chat_id = {update.message.chat.id}, '
                 f'Выполнена функция - unknown, '
                 f'текст_сообщения = {update.message.text}')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


