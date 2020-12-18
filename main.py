import telegram
from telegram.ext import Updater
import logging
import datetime

bot = telegram.Bot(token='1440425473:AAGgDLB3-dihOgOagG5mVfktEzJVhWEDc0g')
updater = Updater(token='1440425473:AAGgDLB3-dihOgOagG5mVfktEzJVhWEDc0g', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я бот и только начинаю "
                                                                    "развиваться. В будущем я захвачу "
                                                                    "человечество!!!")


print(datetime.datetime.today().strftime('%m/%d/%Y %H:%M'))