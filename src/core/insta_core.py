#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

import sys
from time import sleep

from PIL import Image
import random

from PIL import ImageFilter

from core.function.image_handler import watermarkimage
from core.function.log_handler import LogHandler
from dal.instagram_repository import *
from random import shuffle


class InstaBot:
    """
    Instagram bot v 1.0
    like_per_day=1000 - How many likes set bot in one day.

    media_max_like=10 - Don't like media (photo or video) if it have more than
    media_max_like likes.

    media_min_like=0 - Don't like media (photo or video) if it have less than
    media_min_like likes.

    tag_list = ['cat', 'car', 'dog'] - Tag list to like.

    max_like_for_one_tag=5 - Like 1 to max_like_for_one_tag times by row.

    log_mod = 0 - Log mod: log_mod = 0 log to console, log_mod = 1 log to file,
    log_mod = 2 no log.

    https://github.com/LevPasha/instabot.py
    """

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_query = 'https://www.instagram.com/query/'
    url_media = 'https://www.instagram.com/p/'
    url_query_Get = 'http://i.instagram.com/api/v1/'
    url_topsearch = 'https://www.instagram.com/web/search/topsearch/'

    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'en-US,en;q=0.8,fa;q=0.6,nb;q=0.4'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    root_dir = ""

    instagram_repository = ""

    # All counter.
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0

    # List of user_id, that bot follow
    bot_follow_list = []

    my_user_id = ""

    # Log setting.
    log_file_path = ''
    log_file = 0

    log_handler = ""

    # Other.
    media_by_tag = 0
    login_status = False

    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self, login, password,
                 tag_list=['cat', 'car', 'dog'],
                 location_list=[],
                 page_list=[],
                 filter_strings=[],
                 min_likes_count=1000,
                 day_ago = 2,
                 log_mod=0):

        self.bot_start = datetime.datetime.now()
        self.time_in_day = 24 * 60 * 60

        # Auto mod seting:
        # Default list of tag.
        self.tag_list = tag_list

        self.location_list = location_list

        self.page_list = page_list

        self.filter_strings = filter_strings

        self.min_likes_count = min_likes_count

        self.days_ago = day_ago
        # Get random tag, from tag_list, and like (1 to n) times.

        # log_mod 0 to console, 1 to file
        self.log_mod = log_mod

        self.log_handler = LogHandler(log_mod=0, log_file="", log_file_path="")

        self.s = requests.Session()
        # if you need proxy make something like this:
        # self.s.proxies = {"https" : "http://proxyip:proxyport"}
        # by @ageorgios

        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password

        self.media_by_tag = []
        self.media_by_tag_total = []
        # self.users_to_ollow = []

        self.my_user_id = 3665662410

        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.0.1 started at %s:\n' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))

        self.root_dir = os.path.dirname(__file__)

        self.instagram_repository = instagram_repository()

        # print(os.path.join(self.root_dir, os.path.realpath('cdn/image/play.png')))
        # ffff = os.path.join(self.root_dir, os.path.realpath('cdn/content/insta/' + "cdsvsv"))
        # print(ffff)
        # print(os.path.join(ffff,  "csccs.knsd"))

        # print(os.path.normpath('image/play.png'))
        # return
        self.log_handler.write_log(log_string)
        self.login()

        # signal.signal(signal.SIGTERM, self.cleanup)
        # atexit.register(self.cleanup)

    def randomize_list(self):
        # shuffle(self.users_to_ollow)
        shuffle(self.media_by_tag)

    def get_user_id(self, username):
        try:
            # username = self.user_login
            getReq = requests.get(
                'https://www.instagram.com/web/search/topsearch/?context=blended&query=' + username + '')
            parsedget = getReq.json()['users']
            for x in parsedget:
                usr = x['user']
                usrnm = usr['username']
                if (username == usrnm):
                    return str(usr['pk'])
        except:
            self.log_handler.write_log(" Error get_user_id: %s %s" % (username, sys.exc_info()[0]))
            return None

    def get_post_media(self, postid, page):
        try:

            r2 = self.s.get(self.url_media + postid + "?taken-by=" + page + "&__a=1")
            parsed = r2.json()
            media = parsed.get('graphql').get('shortcode_media')
            return media
        except:
            self.log_handler.write_log(" Error get_post_media: %s" % page)
            return None

    def get_user_media(self, userid, page):
        list = []
        try:
            # payload_media = 'q=ig_user(' + userid + ')+%7B+media.after(1%2C+40)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow'
            # r2 = self.s.post(self.url_query, data=payload_media)
            # parsed = r2.json()
            count = str(12)
            # r = self.s.get(
            #     "https://www.instagram.com/graphql/query/?query_id=17862015703145017&variables=%7B%22id%22%3A%22"+userid+"%22%2C%22first%22%3A"+count+"%2C%22")
            r = self.s.get("https://www.instagram.com/graphql/query/?query_id=17862015703145017&variables=%7B%22id%22"
                           "%3A%22" + userid + "%22%2C%22first%22%3A" + count + "%7D")
            parsedRequest = r.json()
            cur = parsedRequest['data']['user']['edge_owner_to_timeline_media']['edges']
            date_yesterday = time.time() - (self.days_ago * 86400)
            for xx in cur:
                xx = xx["node"]
                media_body = xx['edge_media_to_caption']['edges'][0]['node']['text']
                if not self.is_content_allowed(media_body):
                    continue
                likes_count = xx['edge_liked_by']['count']
                if likes_count > self.min_likes_count and  xx['taken_at_timestamp'] > date_yesterday:
                    video_url = None
                    if xx['is_video']:
                        media = self.get_post_media(xx['shortcode'], page)
                        video_url = media["video_url"]
                    list.append({
                        'page': page,
                        'id': xx['shortcode'],
                        'ownerid': xx['owner']['id'],
                        'body': media_body,
                        'mediaurl': xx['display_url'],
                        'thumbnail_src': xx['thumbnail_src'],
                        'likes': xx['edge_liked_by']['count'],
                        'comments': xx['edge_media_to_comment']['count'],
                        'date': xx['taken_at_timestamp'],
                        'dimensions': xx['dimensions'],
                        'is_video': xx['is_video'],
                        'video_url': video_url
                    })

                    # print(usr.get('username') + ' : ' + usr.get('id'))
        except:
            self.log_handler.write_log(" Error get_user_media: %s %s" % (page, sys.exc_info()[0]))
            return list
        return list

    def get_home_timeline_media(self):
        list = []
        try:
            # payload_media = 'q=ig_user(' + userid + ')+%7B+media.after(1%2C+40)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=users%3A%3Ashow'
            # r2 = self.s.post(self.url_query, data=payload_media)
            # parsed = r2.json()
            r = self.s.get(
                "https://www.instagram.com/graphql/query/?query_id=17882195038051799&fetch_media_item_count=500")
            parsedRequest = r.json()

            cur = parsedRequest['data']['user']['edge_web_feed_timeline']['edges']
            for xx in cur:
                xx = xx["node"]
                media_body = xx['edge_media_to_caption']['edges'][0]['node']['text']
                if not self.is_content_allowed(media_body):
                    continue
                likes_count = xx['edge_media_preview_like']['count']
                if likes_count > self.min_likes_count:
                    video_url = None
                    if xx['is_video']:
                        video_url = xx["video_url"]
                    list.append({
                        'page': xx['owner']['username'],
                        'id': xx['shortcode'],
                        'ownerid': xx['owner']['id'],
                        'body': xx['edge_media_to_caption']['edges'][0]['node']['text'],
                        'mediaurl': xx['display_url'],
                        'thumbnail_src': xx['display_url'],
                        'likes': likes_count,
                        'comments': xx['edge_media_to_comment']['count'],
                        'date': xx['taken_at_timestamp'],
                        'dimensions': xx['dimensions'],
                        'is_video': xx['is_video'],
                        'video_url': video_url
                    })

                    # print(usr.get('username') + ' : ' + usr.get('id'))
        except:
            self.log_handler.write_log(" Error get_user_media: %s" % (sys.exc_info()[0]))
            return list
        return list

    def get_location_media(self, locid):
        list = []
        try:
            payload_media = 'q=ig_location(213031810)+%7B+media.after(1307387895988098997%2C+60)+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=locations%3A%3Ashow'
            r2 = self.s.post(self.url_query, data=payload_media)
            parsed = r2.json()
            cur = parsed.get('media').get('nodes')
            for xx in cur:
                list.append({
                    'code': xx['code'],
                    'likes': xx['likes'],
                    'ownerid': xx["owner"]["id"]
                })
                # print(usr.get('username') + ' : ' + usr.get('id'))
        except:
            self.log_handler.write_log(" Error get_location_media: %s" % locid)
            return list
        return list

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        self.log_handler.write_log(log_string)
        self.s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})
        self.login_post = {'username': self.user_login,
                           'password': self.user_password}
        self.s.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self.accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/',
                               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'accept': '*/*',
                               'User-Agent': self.user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(self.url_login, data=self.login_post,
                            allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
                log_string = '%s login success!' % (self.user_login)
                self.log_handler.write_log(log_string)

                # my_userid = self.get_user_id(self.user_login)
                # self.my_followers = []
                # for x in self.get_followers(my_userid):
                #     self.my_followers.append(x)

                # for index, x in enumerate(self.get_followings(my_userid)):
                #     self.bot_follow_list.append([x, time.time() - self.follow_time + index * 60 * 1])

                # self.log_handler.write_log('my_followers fetched successfully!')
            else:
                self.login_status = False
                self.log_handler.write_log('Login error! Check your login data!')
        else:
            self.log_handler.write_log('Login error! Connection error!')

    def logout(self):
        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' % \
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        self.log_handler.write_log(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' % (work_time)
        self.log_handler.write_log(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            self.log_handler.write_log("Logout success!")
            self.login_status = False
        except:
            self.log_handler.write_log("Logout error!")


    def get_followings(self):
        try:

            count = str(100)
            r = self.s.get("https://www.instagram.com/graphql/query/?query_id=17874545323001329&variables=%7B%22id%22"
                           "%3A%22" + str(self.my_user_id) + "%22%2C%22first%22%3A" + count + "%7D")
            parsed_request = r.json()
            cur = parsed_request['data']['user']['edge_follow']['edges']
            for xx in cur:
                xx = xx["node"]
                username = xx["username"]
                if username not in self.page_list:
                    self.page_list.append(username)
        except:
            self.log_handler.write_log(" Error get_user_media: %s" % (sys.exc_info()[0]))
            return list
        return list

    def get_media_id_by_tag(self, tag):
        """ Get media ID set, by your hashtag """

        if self.login_status:
            log_string = "Get media id by tag: %s" % (tag)
            self.log_handler.write_log(log_string)
            if self.login_status == 1:
                url_tag = '%s%s%s' % (self.url_tag, tag, '/')
                try:
                    if tag != 'notag':
                        r = self.s.get(url_tag)
                        text = r.text

                        finder_text_start = ('<script type="text/javascript">'
                                             'window._sharedData = ')
                        finder_text_start_len = len(finder_text_start) - 1
                        finder_text_end = ';</script>'

                        all_data_start = text.find(finder_text_start)
                        all_data_end = text.find(finder_text_end, all_data_start + 1)
                        json_str = text[(all_data_start + finder_text_start_len + 1) \
                            : all_data_end]
                        all_data = json.loads(json_str)

                        # media_by_tag = list(all_data['entry_data']['TagPage'][0] \
                        #                         ['tag']['media']['nodes'])[:10]

                        media_by_tag = list(all_data)

                        for media in media_by_tag:
                            self.add_media_to_list(media)
                            # for x in self.get_followers(media['owner']['id']):
                            #     self.add_to_users_to_follow_list(x)
                            # for x in self.get_commenters(media['code']):
                            #     self.add_to_users_to_follow_list(x)
                            # for x in self.get_likers(media['id'],media['owner']['id']):
                            #     self.add_to_users_to_follow_list(x)

                    for loc in self.location_list:
                        for media in self.get_location_media(loc):
                            self.add_media_to_list(media)
                            # time.sleep(300)
                            # self.add_to_users_to_follow_list(media["ownerid"])
                            # for x in self.get_commenters(media['code']):
                            #     self.add_to_users_to_follow_list(x)
                    # for media in self.get_home_timeline_media():
                    #     self.add_media_to_list(media)
                    #     self.log_handler.write_log("Add Media to list : %s" % media)

                    for page in self.page_list:
                        self.log_handler.write_log("Get media id of: %s" % page)
                        userid = self.get_user_id(page)
                        # if userid != None:
                        # for x in self.get_followers(userid):
                        #     self.add_to_users_to_follow_list(x)
                        # i = 1

                        i = 1
                        for media in self.get_user_media(userid, page):
                            self.add_media_to_list(media)
                            self.log_handler.write_log("Add Media to list : %s %s" % (page, i))
                            i += 1
                            # time.sleep(300)
                            # for xx in self.get_commenters(media['code']):
                            #     self.add_to_users_to_follow_list(xx)
                            # for xx in self.get_likers(media['id'], media['owner']['id']):
                            #     self.add_to_users_to_follow_list(xx)

                    # users_to_allow_shuffled = self.users_to_ollow[:100]
                    # for userid in users_to_allow_shuffled:
                    #     for x in self.get_user_media(userid):
                    #         self.add_media_to_list(x)

                    self.randomize_list()
                    self.log_handler.write_log("Randomize List...")
                except Exception as e:
                    print(e)
                    self.media_by_tag = []
                    self.log_handler.write_log("Except on get_media!")
                    time.sleep(60)
            else:
                return 0

    # def add_to_users_to_follow_list(self, str_to_add):
    #     if str_to_add not in self.users_to_ollow:
    #         self.users_to_ollow.append(str(str_to_add))

    def add_media_to_list(self, str_to_add):
        if str_to_add not in self.media_by_tag:
            self.media_by_tag.append(str_to_add)

    def add_media_to_list_total(self, to_add):
        if to_add not in self.media_by_tag_total:
            self.media_by_tag_total.append(to_add)

    def is_content_allowed(self, media_body):
        isvalid = True
        for filter_str in self.filter_strings:
            if filter_str in media_body:
                isvalid = False
                break
        return isvalid

    def new_auto_mod(self):
        while True:
            # ------------------- Get media_id -------------------
            if len(self.media_by_tag) == 0:  # or len(self.users_to_ollow) == 0:
                self.get_followings()
                self.get_media_id_by_tag(random.choice(self.tag_list))
                self.insert_to_db()
                self.media_by_tag = []

                # self.this_tag_like_count = 0
                # self.max_tag_like_count = random.randint(1, self.max_like_for_one_tag)

            # # ------------------- Like -------------------
            # self.new_auto_mod_like()
            # # ------------------- Follow -------------------
            # self.new_auto_mod_follow()
            # # ------------------- Unfollow -------------------
            # self.new_auto_mod_unfollow()
            # # ------------------- Comment -------------------
            # self.new_auto_mod_comments()

            # Bot iteration in 3600 sec
            sleep_time = 600
            self.log_handler.write_log("Sleeping %s seconds..." % sleep_time)
            time.sleep(sleep_time)
            # print("Tic!")

    def insert_to_db(self):
        self.log_handler.write_log("insert_to_db starts! %s items!" % len(self.media_by_tag))
        for media in self.media_by_tag:
            # if media["id"] == "BO612RJAc-s": post test
            try:
                if not self.is_content_allowed(media["body"]):
                    continue
                self.log_handler.write_log("insert_to_db media id : %s" % media['id'])
                directory = os.path.join(self.root_dir, os.path.realpath('cdn/content/insta/' + media['id']))
                if not os.path.exists(directory):
                    os.makedirs(directory)

                file_name_thumbnail = 'thumbnail_' + media['id'] + ".jpg"
                file_path_thumbnail = os.path.join(directory, file_name_thumbnail)

                if not os.path.exists(file_path_thumbnail):
                    urllib.request.urlretrieve(media['thumbnail_src'], file_path_thumbnail)

                thumb_image = Image.open(file_path_thumbnail)
                thumb_image_width = 400
                thumb_image_height = int((thumb_image_width / thumb_image.width) * thumb_image.height)
                thumb_size = thumb_image_width, thumb_image_height
                if media["is_video"]:
                    thumb_image = thumb_image.resize(thumb_size).filter(ImageFilter.GaussianBlur(radius=5))
                    thumb_image.save(file_path_thumbnail)
                    play_image_path = os.path.join(self.root_dir, os.path.realpath('cdn/image/play.png'))
                    watermarkimage(file_path_thumbnail, play_image_path)
                else:
                    thumb_image = thumb_image.resize(thumb_size)
                    thumb_image.save(file_path_thumbnail)

                thumbnail = {}
                thumbnail["image_url"] = "/content/insta/" + media['id'] + "/" + file_name_thumbnail
                thumbnail["image_width"], thumbnail["image_height"] = thumb_image.size
                thumbnail["image_aspect_ratio"] = thumbnail["image_width"] / thumbnail["image_height"]

                file_extention = ".jpg"
                download_url = media.get('mediaurl')
                media["media_type"] = 2  ##### Image
                if media["is_video"]:
                    file_extention = ".mp4"
                    download_url = media['video_url']
                    media["media_type"] = 3  ##### Video

                file_name = media['id'] + file_extention
                file_path = os.path.realpath(directory + '/' + file_name)

                if not os.path.exists(file_path):
                    urllib.request.urlretrieve(download_url, file_path)

                media["thumbnail"] = thumbnail
                try:
                    self.instagram_repository.upsert_instagram_post(media, file_name)
                    sleep(1)
                except:
                    self.log_handler.write_log("Error: upsert_instagram_post : %s" % media['id'])
                    raise
            except:
                self.log_handler.write_log("Error: insert_to_db media id : %s" % media['id'])

                # print(media)

        self.log_handler.write_log("insert_to_db End!")

    def add_time(self, time):
        """ Make some random for next iteration"""
        return time * 0.9 + time * 0.2 * random.random()
