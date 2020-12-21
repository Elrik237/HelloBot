from telegram.ext import Updater, CommandHandler,InlineQueryHandler, MessageHandler, Filters
from all_functions import start, time_now, caps, echo, unknown, inline_time_now
import os

def main():
    updater = Updater(token=os.environ['token_bot'], use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('time_now', time_now))
    dispatcher.add_handler(CommandHandler('caps', caps))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(InlineQueryHandler(inline_time_now))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()