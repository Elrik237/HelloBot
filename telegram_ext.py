import logging


def catch_exceptions(func):
    def wrapper(self, update, context):
        try:
            return func(self, update, context)
        except Exception as error:
            logging.error(f'Произошла ошибка: {error}')
            context.bot.send_message(chat_id=139664901, text=f'Произошла ошибка: {error}')

    return wrapper
