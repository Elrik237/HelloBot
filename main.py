import logging

from coffee_cat_bot import CoffeeCatBot
from my_logging import initialize_logger


def main():
    try:
        coffee_cat_bot = CoffeeCatBot()
        logging.info('Погнали!')
        coffee_cat_bot.updater.idle()
    except KeyError:
        logging.info('Добавь token, или я не буду работать!')
    except Exception as error:
        logging.error(f'Произошла ошибка: {error}')
        CoffeeCatBot().send_error(error)


if __name__ == '__main__':
    initialize_logger()
    main()
