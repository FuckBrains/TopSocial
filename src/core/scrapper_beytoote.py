import urllib

import os
from time import sleep

import pytz
import sys
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup
from initial_setup import post_installclass
from khayyam import JalaliDatetime, TehranTimezone

from core.function.image_handler import watermarkimage
from core.function.log_handler import LogHandler
from dal.news_repository import NewsRepository


class BeytooteScrapper:
    posts_to_add = []
    posts_to_add_urls = []
    popular_news_url = "http://www.beytoote.com/hotnews.html"
    custom_hashtags = ["اخبار"]

    def __init__(self):
        # self.url = "http://www.beytoote.com/news/sporty-news/fanews3390.html"
        self.log_handler = LogHandler(log_mod=0, log_file="", log_file_path="")
        self.root_dir = os.path.dirname(__file__)
        self.news_repository = NewsRepository()

    def read_single_post(self, post_url):

        post = {}

        post["id"] = post_url[post_url.rfind("/") + 1:post_url.rfind(".")]

        fp = urllib.request.urlopen(post_url)
        my_bytes = fp.read()

        page = my_bytes.decode("utf8")
        fp.close()
        soup = BeautifulSoup(page, 'html.parser')
        post["title"] = soup.select("#content h2 a")[0]
        abstract = soup.select("#content .box-note")[0]

        source_date = soup.select("#content .published")[0].getText().replace('تاریخ انتشار :  ', "") \
            .replace('\n', "") \
            .replace('\t', "")
        shamsi_date = JalaliDatetime.strptime(source_date, '%A, %d %B %Y %H:%M')
        shamsi_datexx = JalaliDatetime(shamsi_date.year, shamsi_date.month, shamsi_date.day, shamsi_date.hour,
                                       shamsi_date.minute, shamsi_date.second, 0, TehranTimezone())

        source_date_utc = shamsi_datexx.todatetime().astimezone(pytz.timezone('UTC'))
        # localtime_shamsi_date = local.localize(source_date_local, is_dst=None)

        image_src = soup.select("#content p.imgarticle img")[0]["src"]
        post["source_media_url"] = "http://beytoote.com/" + image_src
        main_image_file_name = post["source_media_url"][post["source_media_url"].rfind("/") + 1:]
        post["media_type"] = 2

        all_paragraphs = soup.select("#content p")
        post["body"] = ""
        for p in all_paragraphs:
            paragraph_text = p.getText().strip()
            if len(paragraph_text) > 0:
                post["body"] = post["body"] + paragraph_text + "\n"
                # print(paragraph_text)

        post["date"] = source_date_utc
        return post
        # print(source_date)
        # now = JalaliDatetime.strptime("جمعه, 16 تیر 1396 22:26", '%A, %d %b %Y %H:%M')
        # print(source_date_utc)

    def insert_to_db(self):
        for post_url in self.posts_to_add_urls:
            post = self.read_single_post(post_url)
            is_video = False
            self.log_handler.write_log("insert_to_db tweet id : %s" % post['id'])
            directory = os.path.join(self.root_dir, os.path.realpath('cdn/content/news/btt_' + post['id']))
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name_thumbnail = 'thumbnail_' + post['id'] + ".jpg"
            file_path_thumbnail = os.path.join(directory, file_name_thumbnail)

            file_name = None
            post["media_type"] = 1
            has_media = True
            if has_media:
                if not os.path.exists(file_path_thumbnail):
                    urllib.request.urlretrieve(post["source_media_url"], file_path_thumbnail)

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
                thumbnail["image_url"] = "/content/news/btt_" + post['id'] + "/" + file_name_thumbnail
                thumbnail["image_width"], thumbnail["image_height"] = thumb_image.size
                thumbnail["image_aspect_ratio"] = thumbnail["image_width"] / thumbnail["image_height"]

                file_extention = ".jpg"

                post["media_type"] = 2  ##### Image
                if is_video:
                    file_extention = ".mp4"
                    # download_url = tweet["extended_entities"]["media"][0]["video_info"]["variants"][1]["url"]
                    # tweet["media_type"] = 3  ##### Video

                file_name = post['id'] + file_extention
                file_path = os.path.realpath(directory + '/' + file_name)

                if not os.path.exists(file_path):
                    urllib.request.urlretrieve(post["source_media_url"], file_path)

                main_image = Image.open(file_path)

                post["media_width"] = main_image.width
                post["media_height"] = main_image.height
                post["media_aspect_ratio"] = post["media_width"] / post["media_height"]

                post["thumbnail"] = thumbnail

                post["source_owner_id"] = "beytoote"
                post["source_owner_alias"] = "beytoote"
                post["source_owner_title"] = "بیطوطه"

            try:
                self.news_repository.upsert_news_post(post, file_name, self.custom_hashtags)
                sleep(1)
            except:
                self.log_handler.write_log("Error: upsert_twitter_post : %s" % post['id_str'])
                raise

    def get_popular_news(self):
        try:
            fp = urllib.request.urlopen(self.popular_news_url)
            my_bytes = fp.read()

            page = my_bytes.decode("utf8")
            fp.close()
            news_to_add = []
            soup = BeautifulSoup(page, 'html.parser')
            links = soup.select(".hot-news .allmode_topitem .allmode_title a")

            self.log_handler.write_log("%s Tweets to insert..." % len(news_to_add))

            for link in links:
                self.posts_to_add_urls.append("http://beytoote.com" + link["href"])



                # print(tweet_to_add )
        except:
            self.log_handler.write_log("Error: get_home_tweets=> %s" % sys.exc_info()[0])

    def auto_mod(self):
        # while True:
        if len(self.posts_to_add) == 0:  # or len(self.users_to_ollow) == 0:
            self.get_popular_news()
            self.insert_to_db()
            self.posts_to_add = []
            self.posts_to_add_urls = []

        # Bot iteration in 3600 sec
        sleep_time = 500
        self.log_handler.write_log("Sleeping %s seconds..." % sleep_time)
        sleep(sleep_time)


        # -----------------------------------------------------------------------
        # loop through each of my statuses, and print its content
        # -----------------------------------------------------------------------
        # for status in statuses:
        #     print("(%s) @%s %s" % (status["created_at"], status["user"]["screen_name"], status["text"]))


if __name__ == '__main__':
    ff = BeytooteScrapper()
    ff.auto_mod()
