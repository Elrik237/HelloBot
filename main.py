import all_functions
import my_logging
import os
from statistics import Statistic
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters, CallbackQueryHandler

logger = my_logging.get_logger(__name__)  # TODO


def main():
    updater = Updater(token=os.environ['token_bot'], use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', all_functions.start))
    dispatcher.add_handler(CommandHandler('time_now', all_functions.time_now))
    dispatcher.add_handler(CommandHandler('stat', Statistic().stat))
    dispatcher.add_handler(CommandHandler("cat", all_functions.sendcat))
    dispatcher.add_handler(CommandHandler("coffee", all_functions.coffee))
    dispatcher.add_handler(CallbackQueryHandler(all_functions.get_callback_from_button))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), all_functions.echo))
    dispatcher.add_handler(MessageHandler(Filters.command, all_functions.unknown))
    dispatcher.add_handler(InlineQueryHandler(all_functions.inline_))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    my_logging.get_logger(__name__) # TODO Посмотреть логер Гоши
    main()
