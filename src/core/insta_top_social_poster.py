from time import sleep

from core.insta_poster import InstaPoster


def start():
    while True:
        try:
            caption_end_phrase ="مطالب بیشتر در کانال های تلگرام: \n" \
                                "کانال تلگرام سرگرمی: \n" \
                                "https://t.me/topsocial_official \n" \
                                "کانال تلگرام خبری: \n"\
                                "https://t.me/topsocial_news" \

            bot = InstaPoster(
                username="topsocial.com",
                password="",
                caption_end_phrase=caption_end_phrase
            )
            bot.start_top_social_poster("[2]", 3000)  # 2,3 means telegram and twitter
        except:
            sleep(1)
            print("start_top_social_poster Error")
            pass
        else:
            break


# root_dir = os.path.dirname(__file__)
start()
