#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages. This is built on the API wrapper, see
# echobot2.py to see the same example built on the telegram.ext bot framework.
# This program is dedicated to the public domain under the CC0 license.

import logging

import sys
import telegram
from PIL import ImageFilter
from telegram.error import NetworkError, Unauthorized
from time import sleep

from core.function.image_handler import watermarkimage
from PIL import Image

from core.function.log_handler import LogHandler
from core.google.urlshortener import GoogleUrlShortener
from dal.telegram_repository import *
from dal.main_repository import *


class TelegramBot:
    update_id = None
    caption_cache = {}
    root_dir = ""
    log_handler = ""
    telegram_repository = ""
    main_repository = ""
    google_url_shortener = ""

    bot_token = ""
    bot = ""

    def __init__(self,
                 bot_token):

        self.bot_token = bot_token
        self.telegram_repository = telegram_repository()
        self.google_url_shortener = GoogleUrlShortener()
        self.main_repository = main_repository()
        self.log_handler = LogHandler(log_mod=0, log_file="", log_file_path="")
        self.root_dir = os.path.dirname(__file__)

    def start_top_social(self):
        global update_id
        # Telegram Bot Authorization Token

        self.bot = telegram.Bot(self.bot_token)

        # get the first pending update_id, this is so we can skip over it in case
        # we get an "Unauthorized" exception.
        try:
            update_id = self.bot.getUpdates()[0].update_id
        except IndexError:
            update_id = None

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        while True:
            try:
                self.top_social_feed()
            except NetworkError:
                # self.log_handler.write_log("Error: top_social_feed NetworkError...")
                sleep(1)
            except Unauthorized:
                # self.log_handler.write_log("Error: top_social_feed Unauthorized...")
                # The user has removed or blocked the bot.
                update_id += 1

    def top_social_feed(self):
        self.log_handler.write_log("top_social_feed started...")
        # best_video_frame("""D:\projects\godir\src\\topsocial\src\cdn\content\\telegram\-1001000737610_113\\113.mp4""")
        ##### imageio.plugins.ffmpeg.download()
        global update_id
        # Request updates after the last update_id
        for update in self.bot.getUpdates(offset=update_id, timeout=50):
            self.log_handler.write_log("top_social_feed getting updates...")
            # chat_id is required to reply to any message
            # chat_id = update.message.chat_id
            update_id = update.update_id + 1

            if update.message:  # your bot can receive updates without messages
                media = {}
                text = update.message.text.lower()
                if text.startswith("topsocial>"):
                    # media["media_width"], \
                    # media["media_height"], \
                    # media["thumbnail"], \
                    # media["media_aspect_ratio"] = ""
                    media["id"] = str(update.message.chat_id) \
                                  + "_" \
                                  + str(update.message.message_id)
                    title_and_body = text.replace("topsocial>", "").split("&&&")
                    if len(title_and_body) < 2:
                        update.message.reply_text(
                            "The title and body is required!")
                        return
                    media["title"] = title_and_body[0]
                    media["body"] = title_and_body[1]
                    media["media_type"] = 1  #### Enum Posttype >> "Text"
                    self.telegram_repository.upsert_telegram_post(update.message, None, media)
                    sleep(1)
                else:
                    if update.message['forward_from_chat'] is None and update.message['forward_from'] is None:
                        #### This is the next post title
                        destination_message_id = update.message.message_id + 1
                        self.caption_cache[destination_message_id] = update.message.text
                        return

                    if not self.caption_cache.get(update.message["message_id"]):
                        sleep(1)
                        if not self.caption_cache.get(update.message["message_id"]):
                            update.message.reply_text(
                                "You should forward from a channel or group! and also caption is required... ")
                            return

                    if self.caption_cache.get(update.message.message_id) is None:
                        update.message.reply_text("Cache Not Found! ")
                        return

                    media_id_part_one = update.message['forward_from_chat']["id"] \
                        if update.message['forward_from_chat'] is not None else \
                        update.message['forward_from']["id"]
                    media["id"] = str(media_id_part_one) \
                                  + "_" \
                                  + str(update.message.message_id)

                    directory = os.path.join(self.root_dir, os.path.realpath('cdn/content/telegram/' + media["id"]))
                    print(directory)
                    has_video = not bool(not update.message.video)
                    has_photo = not bool(not update.message.photo)
                    has_document = not bool(not update.message.document)
                    if has_video:
                        media_type = 3  #### Enum Posttype >> "Video"
                    elif has_photo:
                        media_type = 2  #### Enum Posttype >> "Image"
                    else:
                        media_type = 3  #### Enum Posttype >> "Document" BUT MARKED AS 3 BECAUSE TELEGRAM STORES THE GIFS AS MP4

                    media["media_type"] = media_type

                    media["media_width"], \
                    media["media_height"], \
                    file_name, \
                    media["thumbnail"] = self.download_file_by_id(has_video, has_photo, has_document, directory,
                                                                  media["id"],
                                                                  update.message)
                    media["media_aspect_ratio"] = media["media_width"] / media["media_height"]
                    media["title"] = self.caption_cache[update.message.message_id]
                    media["body"] = None
                    self.caption_cache.pop(update.message.message_id)

                    self.telegram_repository.upsert_telegram_post(update.message, file_name, media)
                    sleep(1)
                    # Reply to the message
                update.message.reply_text("Saved Successfully!")

    def download_file_by_id(self, has_video, has_photo, has_document, directory, postid, message):
        thumbnail = {}
        file_extension = ".mp4"

        if has_video:
            file_id = message.video.file_id
            file_id_thumbnail = message.video["thumb"].file_id

        elif has_photo:
            file_extension = ".jpg"
            file_id_thumbnail = message.photo[-1].file_id
            file_id = file_id_thumbnail
        elif has_document:
            file_id = message.document.file_id
            file_id_thumbnail = message.document["thumb"].file_id
        else:
            return None, None, None, None

        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name_thumbnail = "thumbnail_" + str(message.message_id) + ".jpg"
        file_path_thumbnail = os.path.join(directory, file_name_thumbnail)

        if not os.path.exists(file_path_thumbnail):
            new_file = self.bot.getFile(file_id_thumbnail)
            new_file.download(file_path_thumbnail)
        thumb_image = Image.open(file_path_thumbnail)
        thumb_image_width = 400
        thumb_image_height = int((thumb_image_width / thumb_image.width) * thumb_image.height)
        thumb_size = thumb_image_width, thumb_image_height
        if has_video or has_document:
            thumb_image = thumb_image.resize(thumb_size).filter(ImageFilter.GaussianBlur(radius=5))
            thumb_image.save(file_path_thumbnail)
            play_image_path = os.path.join(self.root_dir, os.path.realpath('cdn/image/play.png'))
            watermarkimage(file_path_thumbnail, play_image_path)
        else:
            thumb_image = thumb_image.resize(thumb_size)
            thumb_image.save(file_path_thumbnail)

        thumbnail["image_url"] = "/content/telegram/" + postid + "/" + file_name_thumbnail
        thumbnail["image_width"], thumbnail["image_height"] = thumb_image.size
        thumbnail["image_aspect_ratio"] = thumbnail["image_width"] / thumbnail["image_height"]

        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = str(message.message_id) + file_extension
        file_path = os.path.realpath(directory + '/' + file_name)
        if not os.path.exists(file_path):
            new_file = self.bot.getFile(file_id)
            new_file.download(file_path)

        media_width = 0
        media_height = 0
        if has_video:
            media_width = message.video.width
            media_height = message.video.height
        elif has_document:
            media_width = message.document.thumb.width * 10
            media_height = message.document.thumb.height * 10
        elif has_photo:
            with Image.open(file_path) as image:
                media_width, media_height = image.size

        return media_width, media_height, file_name, thumbnail

    def start_top_social_poster(self, channel_id, source_network,min_likes_count):
        global update_id
        # Telegram Bot Authorization Token

        self.bot = telegram.Bot(self.bot_token)

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        running = False
        while True:
            try:
                if not running:
                    running = True
                    self.new_posts_to_channel(channel_id, source_network,min_likes_count)
                    running = False
                    sleep(100)
            except NetworkError:
                sleep(500)
            except Unauthorized:
                # self.log_handler.write_log("Error: top_social_feed Unauthorized...")
                # The user has removed or blocked the bot.
                update_id += 1

    def new_posts_to_channel(self, channel_id, source_network,min_likes_count):
        posts = self.main_repository.get_not_posted_to_telegram_channel(source_network,min_likes_count)
        for post in posts:
            try:
                self.google_url_shortener = GoogleUrlShortener()
                self.post_to_channel(post, channel_id)
                self.main_repository.mark_post_as_sent_to_telegram_channel(post)
                sleep(15)
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.log_handler.write_log(
                    "Error: send new_posts_to_channel media id : %s %s, Line: %s" % (
                        post['_key'], sys.exc_info()[0], exc_tb.tb_lineno))

    def post_to_channel(self, post, channel_id):
        try:
            url = ""
            if post.get("urls_extracted") is not None \
                    and len(post["urls_extracted"]) > 0 \
                    and post["urls_extracted"][0].get("state") == 1:
                url = self.google_url_shortener.goo_shorten_url(
                    "http://www.topsocial.com/postexturl/" + post["_key"] + "/0")
            else:
                seo_dashed_url = post["seo_dashed_url"] if post.get("seo_dashed_url") is not None else "پست"
                url = self.google_url_shortener.goo_shorten_url(
                    "https://www.topsocial.com/post/" + seo_dashed_url + "/" + post["_key"])

            url = url + "\n" + channel_id
            if post.get('media_url') is not None:
                file_path = os.path.join(self.root_dir, os.path.realpath('cdn/' + post['media_url']))

                total = 190
                totrim = total - len(url)

                caption = post["title"]
                caption = post["body"] if caption is None else caption
                caption = "" if caption is None else caption
                if caption is not None and len(caption) > totrim:
                    caption = caption[:totrim] + "..."

                caption = caption + "\n" + url

                if post["media_type"] == 2:  ## Image
                    photo = open(file_path, 'rb')
                    self.bot.send_photo(channel_id, photo, caption=caption)
                if post["media_type"] == 3:  ## Video
                    video = open(file_path, 'rb')
                    self.bot.send_video(channel_id, video, caption=caption)
            else:
                self.bot.send_message(channel_id, post["body"] + "\n" + url)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.log_handler.write_log(
                "Error: send post_to_channel media id : %s %s, Line: %s" % (
                    post['_key'], sys.exc_info()[0], exc_tb.tb_lineno))
            raise e

    def write_log(self, log_text):
        """ Write log by print() or logger """

        if self.log_mod == 0:
            try:
                print(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
        elif self.log_mod == 1:
            # Create log_file if not exist.
            if self.log_file == 0:
                self.log_file = 1
                now_time = datetime.datetime.now()
                self.log_full_path = '%s%s_%s.log' % (self.log_file_path,
                                                      self.access_key,
                                                      now_time.strftime("%d.%m.%Y_%H:%M"))
                formatter = logging.Formatter('%(asctime)s - %(name)s '
                                              '- %(message)s')
                self.logger = logging.getLogger(self.access_key)
                self.hdrl = logging.FileHandler(self.log_full_path, mode='w')
                self.hdrl.setFormatter(formatter)
                self.logger.setLevel(level=logging.INFO)
                self.logger.addHandler(self.hdrl)
            # Log to log file.
            try:
                self.logger.info(log_text)
            except UnicodeEncodeError:
                print("Your text has unicode problem!")
