    #!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

from core.insta_core import InstaBot


def start():
    while True:
        try:
            bot = InstaBot(
                login="topsocial.com.news",
                password="",
                tag_list=source_config["instagram"]["hashtags"],
                page_list=source_config["instagram"]["pages"],
                filter_strings=source_config["instagram"]["filter_strings"],
                min_likes_count=source_config["instagram"]["min_likes"],
                day_ago=source_config["instagram"]["days_ago"],
                log_mod=0)
            bot.new_auto_mod()
        except:
            pass
        else:
            break


root_dir = os.path.dirname(__file__)
file_path = os.path.join(root_dir, os.path.realpath('config/social_sources.json'))
with open(file_path, encoding="utf8") as data_file:
    source_config = json.load(data_file)
    start()



