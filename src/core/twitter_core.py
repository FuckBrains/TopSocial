import urllib
import sys

import logging
from time import sleep

from PIL import Image
from PIL import ImageFile
from PIL import ImageFilter
from core.function.image_handler import watermarkimage
from core.function.log_handler import LogHandler
from dal.twitter_repository import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
# -----------------------------------------------------------------------
# twitter-hoome-timeline:
#  - uses the Twitter API and OAuth to log in as your username,
#    and lists the latest 50 tweets from people you are following
# -----------------------------------------------------------------------
import os

from past.builtins import execfile
from twitter import *


class TwitterBot:
    log_file = 0
    log_file_path = ""

    log_mod = 0

    root_dir = ""

    home_feed_count_to_read = 0
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    twitter_api = ""

    log_handler = ""

    tweet_to_add = []

    custom_hashtags = ["اخبار"]

    twitter_repository = ""

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_key,
                 access_secret,
                 home_feed_count_to_read,
                 log_mod=0):

        self.log_mod = log_mod
        self.root_dir = os.path.dirname(__file__)

        self.log_handler = LogHandler(log_mod=0, log_file="", log_file_path="")

        self.twitter_repository = twitter_repository()

        self.home_feed_count_to_read = home_feed_count_to_read
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_key = access_key
        self.access_secret = access_secret

        self.login()

    def unshorten_urls(self, text):
        regexp = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(regexp, text)
        extracted_urls = []
        for url in urls:
            try:
                res = urllib.request.urlopen(url)
                actual_url = res.geturl()
                xframeOptions = res.headers.get("X-Frame-Options")
                state = 1  # iframe
                if xframeOptions is not None and xframeOptions.upper() == "SAMEORIGIN":
                    state = 2  # linkonly
                if "twitter.com" in actual_url \
                        or "t.co" in actual_url \
                        or "t.com" in actual_url \
                        or "10.10.34.34" in actual_url:
                    actual_url = url
                    state = 2

                actual_url_obj = {
                    "url": actual_url,
                    "state": state
                }
                extracted_urls.append(actual_url_obj)
            except:
                actual_url_obj = {
                    "url": url,
                    "state": 2
                }
                extracted_urls.append(actual_url_obj)

        text = re.sub(regexp,
                      "",
                      text)
        return text, extracted_urls

    def insert_to_db(self):
        self.log_handler.write_log("insert_to_db starts! %s items!" % len(self.tweet_to_add))
        for tweet in self.tweet_to_add:
            # if media["id"] == "BO612RJAc-s": post test
            try:

                if tweet.get("retweeted_status") is not None:
                    tweet = tweet["retweeted_status"]

                # TODO: Remove this section if embedded links fulfilled
                if tweet["entities"].get('media') is None:
                    continue

                if len(tweet["urls_extracted"]) == 0:
                    if len(tweet["entities"]["urls"]) > 0:
                        tweet["urls_extracted"] = [{
                            "url": tweet["entities"]["urls"][0]["url"],
                            "state": 2
                        }]

                # if tweet["id_str"].strip() == "865244413739626499":  # DEBUG
                #     print("xx")

                is_video = tweet.get("extended_entities") and tweet["extended_entities"]["media"][0]["type"] == "video"
                self.log_handler.write_log("insert_to_db tweet id : %s" % tweet['id_str'])
                directory = os.path.join(self.root_dir, os.path.realpath('cdn/content/twitter/' + tweet['id_str']))
                if not os.path.exists(directory):
                    os.makedirs(directory)

                file_name_thumbnail = 'thumbnail_' + tweet['id_str'] + ".jpg"
                file_path_thumbnail = os.path.join(directory, file_name_thumbnail)

                file_name = None
                tweet["media_type"] = 1
                if tweet["entities"].get('media') is not None:
                    if not os.path.exists(file_path_thumbnail):
                        urllib.request.urlretrieve(tweet["entities"]['media'][0]["media_url"], file_path_thumbnail)

                    thumb_image = Image.open(file_path_thumbnail)
                    thumb_image_width = 400
                    thumb_image_height = int((thumb_image_width / thumb_image.width) * thumb_image.height)
                    thumb_size = thumb_image_width, thumb_image_height
                    if is_video:  # hasvideo
                        thumb_image = thumb_image.resize(thumb_size).filter(ImageFilter.GaussianBlur(radius=10))
                        thumb_image.save(file_path_thumbnail)
                        play_image_path = os.path.join(self.root_dir, os.path.realpath('cdn/image/play.png'))
                        watermarkimage(file_path_thumbnail, play_image_path)
                    else:
                        thumb_image = thumb_image.resize(thumb_size)
                        thumb_image.save(file_path_thumbnail)

                    thumbnail = {}
                    thumbnail["image_url"] = "/content/twitter/" + tweet['id_str'] + "/" + file_name_thumbnail
                    thumbnail["image_width"], thumbnail["image_height"] = thumb_image.size
                    thumbnail["image_aspect_ratio"] = thumbnail["image_width"] / thumbnail["image_height"]

                    file_extention = ".jpg"
                    download_url = tweet['entities']['media'][0]["media_url"]
                    tweet["media_type"] = 2  ##### Image
                    if is_video:
                        file_extention = ".mp4"
                        download_url = tweet["extended_entities"]["media"][0]["video_info"]["variants"][1]["url"]
                        tweet["media_type"] = 3  ##### Video

                    file_name = tweet['id_str'] + file_extention
                    file_path = os.path.realpath(directory + '/' + file_name)

                    if not os.path.exists(file_path):
                        urllib.request.urlretrieve(download_url, file_path)

                    tweet["thumbnail"] = thumbnail

                try:
                    self.twitter_repository.upsert_twitter_tweet(tweet, file_name,self.custom_hashtags)
                    sleep(1)
                except:
                    self.log_handler.write_log("Error: upsert_twitter_post : %s" % tweet['id_str'])
                    raise
            except Exception as e:
                self.log_handler.write_log("Error: insert_to_db media id : %s %s" % (tweet['id_str'], e))

                # print(media)

        self.log_handler.write_log("insert_to_db End!")

    def login(self):
        # -----------------------------------------------------------------------
        # create twitter API object
        # -----------------------------------------------------------------------
        self.twitter_api = Twitter(
            auth=OAuth(self.access_key,
                       self.access_secret,
                       self.consumer_key,
                       self.consumer_secret))

    def get_home_tweets(self):
        # -----------------------------------------------------------------------
        # request my home timeline
        # twitter API docs: https://dev.twitter.com/rest/reference/get/statuses/home_timeline
        # -----------------------------------------------------------------------
        proxy = 'http://ir236996:711278@us.mybestport.com:443'

        os.environ['http_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        try:
            tweet_to_add = self.twitter_api.statuses.home_timeline(count=self.home_feed_count_to_read)
            self.log_handler.write_log("%s Tweets to insert..." % len(tweet_to_add))
            for media in tweet_to_add:
                media["text"], media["urls_extracted"] = self.unshorten_urls(media["text"])
                self.tweet_to_add.append(media)
                # print(tweet_to_add )
        except:
            self.log_handler.write_log("Error: get_home_tweets=> %s" % sys.exc_info()[0])

        try:
            del os.environ['http_proxy']
        except:
            print("http_proxy env del error")

        try:
            del os.environ['HTTP_PROXY']
        except:
            print("HTTP_PROXY env del error")

        try:
            del os.environ['https_proxy']
        except:
            print("https_proxy env del error")

        try:
            del os.environ['HTTPS_PROXY']
        except:
            print("HTTPS_PROXY env del error")

    def auto_mod(self):
        while True:
            if len(self.tweet_to_add) == 0:  # or len(self.users_to_ollow) == 0:
                self.get_home_tweets()
                self.insert_to_db()
                self.tweet_to_add = []

            # Bot iteration in 3600 sec
            sleep_time = 500
            self.log_handler.write_log("Sleeping %s seconds..." % sleep_time)
            time.sleep(sleep_time)


            # -----------------------------------------------------------------------
            # loop through each of my statuses, and print its content
            # -----------------------------------------------------------------------
            # for status in statuses:
            #     print("(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"]))
