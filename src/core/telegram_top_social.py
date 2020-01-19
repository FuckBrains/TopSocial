from time import sleep
from core.telegram_core import TelegramBot


def start():
    while True:
        try:
            #          @tscl_bot
            bot = TelegramBot(bot_token="")
            bot.start_top_social()
        except:
            sleep(1)
            pass
        else:
            break


# root_dir = os.path.dirname(__file__)
start()

