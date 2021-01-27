from coffee_cat_bot import CoffeeCatBot
from my_logging import initialize_logger


def main():
    coffee_cat_bot = CoffeeCatBot()
    coffee_cat_bot.updater.idle()


if __name__ == '__main__':
    initialize_logger()
    main()
