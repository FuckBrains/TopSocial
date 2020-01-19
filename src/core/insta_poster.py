import os
import sys
from time import sleep

import core.instagram_api
from core.function.log_handler import LogHandler
from core.google.urlshortener import GoogleUrlShortener
from dal.main_repository import main_repository


class InstaPoster:
    def __init__(self,
                 username,
                 password,
                 caption_end_phrase):
        self.username = username
        self.password = password

        self.caption_end_phrase = caption_end_phrase

        self.main_repository = main_repository()

        self.instagram_api = core.instagram_api.InstagramAPI(username, password)
        self.instagram_api.login()  # login

        self.log_handler = LogHandler(log_mod=0, log_file="", log_file_path="")


        self.root_dir = os.path.dirname(__file__)

    def start_top_social_poster(self, source_network,min_likes_count):
        running = False
        while True:
            try:
                if not running:
                    running = True
                    self.new_posts_to_page(source_network,min_likes_count)
                    running = False
                    self.log_handler.write_log("Waiting 300 seconds...")
                    sleep(300)
            except :
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.log_handler.write_log(
                    "Error: start_top_social_poster  : %s, Line: %s" % (sys.exc_info()[0], exc_tb.tb_lineno))
                sleep(500)


    def new_posts_to_page(self, source_network,min_likes_count):
        posts = self.main_repository.get_not_posted_to_instagram(source_network,min_likes_count)
        self.log_handler.write_log("Starting for %s posts..."%str(len(posts)))
        for post in posts:
            try:
                self.google_url_shortener = GoogleUrlShortener()
                self.post_to_page(post)
                self.main_repository.mark_post_as_sent_to_instagram(post)
                sleep(300)
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.log_handler.write_log(
                    "Error: send new_posts_to_channel media id : %s %s, Line: %s" % (
                        post['_key'], sys.exc_info()[0], exc_tb.tb_lineno))


    def post_to_page(self, post):
        try:
            url = "\n"+"@"+ self.username + "\n "
            # if post.get("urls_extracted") is not None \
            #         and len(post["urls_extracted"]) > 0 \
            #         and post["urls_extracted"][0].get("state") == 1:
            #     url = url+ self.google_url_shortener.goo_shorten_url(
            #         "http://www.topsocial.com/postexturl/" + post["_key"] + "/0")
            # else:
            #     seo_dashed_url = post["seo_dashed_url"] if post.get("seo_dashed_url") is not None else "پست"
            #     url = url + self.google_url_shortener.goo_shorten_url(
            #         "https://www.topsocial.com/post/" + seo_dashed_url + "/" + post["_key"])

            url = url+ self.caption_end_phrase
            if post.get('media_url') is not None:
                file_path = os.path.join(self.root_dir, os.path.realpath('cdn/' + post['media_url']))


                total = 2000
                totrim = total - len(url)

                caption = post.get("body")
                caption = post["title"] if (caption is None and post.get("title") is not None) else caption
                caption = "" if caption is None else caption
                if caption is not None and len(caption) > totrim:
                    caption = caption[:totrim] + "..."

                caption = caption + "\n" + url

                if post["media_type"] == 2:  ## Image
                    # photo = open(file_path, 'rb')
                    self.post_photo(file_path, caption=caption)
                if post["media_type"] == 3:  ## Video
                    # video = open(file_path, 'rb')
                    thumbnail_file_path = os.path.join(self.root_dir,
                                                       os.path.realpath('cdn/' + post['thumbnail']["image_url"]))
                    self.post_video(file_path, thumbnail_file_path, caption=caption)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.log_handler.write_log(
                "Error: send post_to_channel media id : %s %s, Line: %s" % (
                    post['_key'], sys.exc_info()[0], exc_tb.tb_lineno))
            raise e



    def post_video(self,video_local_path,thumbnail_local_path,caption):
        try:
            self.instagram_api.uploadVideo(video_local_path, thumbnail_local_path, caption=caption)
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.log_handler.write_log(
                "Error: post_video  : %s, Line: %s" % (sys.exc_info()[0], exc_tb.tb_lineno))


    def post_photo(self,video_local_path,caption):
        self.instagram_api.uploadPhoto(video_local_path,  caption=caption)