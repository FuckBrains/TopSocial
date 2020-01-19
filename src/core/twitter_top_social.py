import os
from time import sleep

import sys

from core.twitter_core import TwitterBot
import time

# topsocial APP
# consumer_key = "3DOfk01VTkuhEa3GwLEfeCBNP"
# consumer_secret = "76U8B1dtwU95clcmKnqZlRDypNLiQNH8YF2CGnYmfpWYsG1NcM"
# access_key = "1593196142-QjaONelVtqMx5hharTrwCJ3bS8jI17mbS0NLtNU"
# access_secret = "1iZSC7KEn19p70lAjfRuQd8s2ucPIackDZ5rRqXziTwzG"

# TOPCL APP
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def start():

    # parsedDate = time.mktime(time.strptime(u'Mon May 22 23:10:44 +0000 2017', "%a %b %d %H:%M:%S +0000 %Y"))
    # print(parsedDate)
    while True:
        try:
            bot = TwitterBot(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_key=access_key,
                access_secret=access_secret,
                home_feed_count_to_read=200,
                log_mod=0)
            bot.auto_mod()
        except Exception as e:
            print("TwitterBot error: %s"% sys.exc_info()[0] )
            sleep(1)
            pass
        else:
            break


root_dir = os.path.dirname(__file__)
start()
