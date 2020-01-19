# from elasticsearch import Elasticsearch
# 
# es = Elasticsearch("192.168.1.112")
# 
# es.indices.create(index='posts', ignore=400)
# 
# 
# def insert_one_if_not_exists(post):
#     es.index(index="posts", doc_type="instapost", body=post, id=post["id"])
import datetime
import time
import re

from main import extract_phrases
from pyArango.connection import *
from khayyam import *
# from summa import keywords
# from core.nlp.summa import keywords
from textrank import *

from core.function.url_handler import SeoUrl


class main_repository:
    conn = ""
    db_name = "tscl"
    col_name_post = "Posts"

    def __init__(self):
        self.conn = Connection(username="tscluser", password="")

    # def db_connect():
    #     conn = Connection(username="root", password=1)



    def initialize_db_collections(self):
        if not self.conn.hasDatabase(self.db_name):
            self.conn.createDatabase(name=self.db_name)
        db = self.conn[self.db_name]
        if not db.hasCollection(self.col_name_post):
            db.createCollection(name=self.col_name_post)

    def upsert_post(self, post, custom_hashtags):
        db = self.conn[self.db_name]
        try:
            _key = post["id"]
            posts_collection = db[self.col_name_post]
            doc = posts_collection[_key]
            doc["date_last_modif"] = int(time.time())
        except KeyError:
            col = db[self.col_name_post]
            doc = col.createDocument()
            doc["_key"] = post["id"]
            doc["date_set"] = int(time.time())

        doc["title"] = post["title"].replace("\n", " ") if post["title"] is not None else None
        doc["body"] = post["body"]

        doc["media_type"] = post["media_type"]
        doc["media_url"] = post["media_url"]
        doc["media_width"] = post["media_width"]
        doc["media_height"] = post["media_height"]
        doc["media_aspect_ratio"] = post["media_aspect_ratio"]

        doc["thumbnail"] = post["thumbnail"]

        doc["comments_count"] = post["comments_count"]
        doc["likes_count"] = post["likes_count"]

        doc["source_date"] = post["source_date"]
        doc["source_date_tehran"] = JalaliDatetime(datetime.datetime.fromtimestamp(post["source_date"])).strftime(
            '%Y%m%d%H%M%S')
        doc["source_media_url"] = post["source_media_url"]
        doc["source_owner_id"] = post["source_owner_id"]
        doc["source_owner_alias"] = post["source_owner_alias"]
        doc["source_owner_title"] = post["source_owner_title"]

        if post.get("urls_extracted") is not None:
            doc["urls_extracted"] = post["urls_extracted"]

        doc["language"] = post["language"]
        doc["source"] = post["source"]

        doc["seo_dashed_url"] = SeoUrl().seo_friendly_url(
            title=post["title"] if post["title"] is not None else post["body"])

        detected_keywords = extract_key_phrases(post["body"].replace("،", " ")) if post[
                                                                                       "body"] is not None else extract_key_phrases(
            post["title"].replace("،", " ") if post["title"] is not None else "")
        post_hashtags = re.findall(r"#(\w+)", post["body"]) if post["body"] is not None else {}
        doc["hashtags"] = list(set().union(detected_keywords, post_hashtags, custom_hashtags))

        doc.save()

    def get_one_by_key(self, _key):
        db = self.conn[self.db_name]
        try:
            doc = db[self.col_name_post][_key]
        except KeyError:
            doc = None
        return doc

    def get_one_post_by_insta_id(self, insta_post_id):
        db = self.conn[self.db_name]
        doc = db[self.col_name_post].fetchDocument()
        return doc

    def get_not_posted_to_telegram_channel(self, source_network, min_likes_count):
        source_network_filter = ""
        if source_network is not None:
            source_network_filter = source_network_filter + " AND (x.source IN " + source_network + ")"
        if min_likes_count is not None:
            source_network_filter = source_network_filter + " AND ((x.likes_count > " + str(
                min_likes_count) + ") OR (x.source == 2))"
        db = self.conn[self.db_name]
        aql = " LET mindate =  DATE_TIMESTAMP(DATE_SUBTRACT(DATE_NOW(), 1, 'day'))/1000 " \
              " FOR x IN " + self.col_name_post + \
              " FILTER (x.posted_to_telegram == null OR x.posted_to_telegram == false) " \
              " AND (x.source_date > mindate) " \
              + source_network_filter + \
              " SORT x.source_date " \
              " LIMIT 100 " \
              " RETURN x "
        return db.AQLQuery(aql, rawResults=True, batchSize=100)

    def mark_post_as_sent_to_telegram_channel(self, doc):
        db = self.conn[self.db_name]
        try:
            doc = db[self.col_name_post][doc["_key"]]
            doc["posted_to_telegram"] = True
            doc.patch()
        except:
            print(datetime.sys.exc_info()[0])

    def get_not_posted_to_instagram(self, source_network, min_likes_count):
        source_network_filter = ""
        if source_network is not None:
            source_network_filter = source_network_filter + " AND ((x.source IN " + source_network + ") OR (x.likes_count > " + str(
                min_likes_count) + "))"

        db = self.conn[self.db_name]
        aql = " LET mindate =  DATE_TIMESTAMP(DATE_SUBTRACT(DATE_NOW(), 1, 'day'))/1000 " \
              " FOR x IN " + self.col_name_post + \
              " FILTER (x.posted_to_instagram == null OR x.posted_to_instagram == false) " \
              "AND (x.media_url != null) " \
              "AND (x.source_date > mindate) " \
              + source_network_filter + \
              " SORT x.source_date " \
              " LIMIT 100 " \
              " RETURN x "
        print(aql)
        return db.AQLQuery(aql, rawResults=True, batchSize=100)

    def mark_post_as_sent_to_instagram(self, doc):
        db = self.conn[self.db_name]
        try:
            doc = db[self.col_name_post][doc["_key"]]
            doc["posted_to_instagram"] = True
            doc.patch()
        except:
            print(datetime.sys.exc_info()[0])
