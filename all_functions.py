from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton
import requests
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
    text = "%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n%s \n" % ("Привет, я бот который только начинает развиваться!",
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


def getcat():
    try:
        r = requests.get('http://thecatapi.com/api/images/get?format=src')
        url = r.url
    except:
        url = getcat()
        print('Error with cat parsing')
        pass
    return url


def sendcat(update, context):
    f = 'cat'
    Statistic().statistic_updata(update, f)
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=getcat(), reply_markup=draw_button())


def draw_button():
    keys = [[InlineKeyboardButton('🐈Еще котика?!🐈', callback_data='2')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)


def coffee(update, context):
    f = 'coffee'
    Statistic().statistic_updata(update, f)
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

    context.bot.send_message(chat_id=update.effective_chat.id, text='Когда вы хотите пригласить @Elrik237 на кофе?',
                             reply_markup=markup)


query_user_id = []


def get_callback_from_button(update, context):
    user = update.effective_user.username
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

    if int(query.data) == 2:
        sendcat(update, context)
    elif int(query.data) == 1:
        time_now(update, context)
    elif int(query.data) == 3:
        coffee(update, context)
    elif int(query.data) == 4:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я сообщил @Elrik237, что вы хотите сегодня встретиться!')
        context.bot.send_message(chat_id=139664901, text=f'{user_id}:@{user} хочет сегодня выпить с вами кофе!',
                                 reply_markup=markup1)
        query_user_id.insert(0, user_id)


    elif int(query.data) == 5:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я сообщил @Elrik237, что вы хотите завтра встретиться!')
        context.bot.send_message(chat_id=139664901, text=f'{user_id}:@{user} хочет завтра выпить с вами кофе!',
                                 reply_markup=markup1)
        query_user_id.insert(0, user_id)


    elif int(query.data) == 6:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Я сообщил @Elrik237, что вы хотите на выходных встретиться!')
        context.bot.send_message(chat_id=139664901, text=f'{user_id}:@{user} хочет на выходных выпить с вами кофе!',
                                 reply_markup=markup1)
        query_user_id.insert(0, user_id)


    elif int(query.data) == 7:
        context.bot.send_message(chat_id=query_user_id[0],
                                 text='@Elrik237 готов с Вами встретиться!')
        context.bot.send_message(chat_id=139664901, text='Я отправил ваш ответ')
    elif int(query.data) == 8:
        context.bot.send_message(chat_id=query_user_id[0],
                                 text='@Elrik237 не готов с Вами встретиться! Давайте запланируем другой день!')
        context.bot.send_message(chat_id=139664901, text='Я отправил ваш ответ')


def echo(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    f = 'echo'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text + ' ' + time)


def time_now(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    f = 'time_now'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text=time)


def inline_(update, context):
    time = datetime.datetime.today().strftime('%m/%d/%Y %H:%M')
    f = 'inlin_'
    Statistic().inline_statistic_updata(update, f)

    results = list()
    results.append(
        InlineQueryResultArticle(
            id='1',
            title='Дата и время',
            description='Выводит текущую дату и врумя',
            input_message_content=InputTextMessageContent('Текущая дата и время: ' + time)
        )
    )
    # results.append(
    #     InlineQueryResultArticle(
    #         id='2',
    #         title='Пригласить на кофе',
    #         description='Приглашает любого участника чата на кофе',
    #         input_message_content=InputTextMessageContent('Когда Вы хотитие пригласить на кофе?'),
    #         reply_markup=InlineKeyboardMarkup(keyboard)
    #
    #     )
    # )
    context.bot.answer_inline_query(update.inline_query.id, results=results)


def unknown(update, context):
    f = 'unknown'
    Statistic().statistic_updata(update, f)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
