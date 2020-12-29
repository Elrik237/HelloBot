import all_functions
import my_logging
import os
from statistics import Statistic
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters

logger = my_logging.get_logger(__name__)


def main():
    updater = Updater(token=os.environ['token_bot'], use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', all_functions.start))
    dispatcher.add_handler(CommandHandler('time_now', all_functions.time_now))
    dispatcher.add_handler(CommandHandler('caps', all_functions.caps))
    dispatcher.add_handler(CommandHandler('stat', Statistic().stat))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), all_functions.echo))
    dispatcher.add_handler(MessageHandler(Filters.command, all_functions.unknown))
    dispatcher.add_handler(InlineQueryHandler(all_functions.inline_time_now))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    my_logging.get_logger(__name__)
    main()
