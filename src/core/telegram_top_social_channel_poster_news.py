from time import sleep
from core.telegram_core import TelegramBot


def start():
    while True:
        try:
            #          @tscl_bot
            bot = TelegramBot(bot_token="")
            bot.start_top_social_poster("@topsocial_news", "[3]",None)
        except:
            sleep(1)
            print("start_top_social_poster Error")
            pass
        else:
            break


# root_dir = os.path.dirname(__file__)
start()
