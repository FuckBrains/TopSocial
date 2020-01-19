from dal.main_repository import *
from core.nlp.summerize_text import *


class twitter_repository:
    main_repository = ""

    def __init__(self):
        self.main_repository = main_repository()

    def upsert_twitter_tweet(self, twitter_tweet, file_name,custom_hashtags):

        # if twitter_tweet["id_str"].strip() == "866353982217699328": # DEBUG
        #     print("xx")
        post = {}
        post["id"] = twitter_tweet["id_str"]

        summaraized_title = summerize_text(twitter_tweet["text"])._text if summerize_text(
            twitter_tweet["text"]) is not None else None
        if summaraized_title is not None and len(summaraized_title) > 70:
            summaraized_title = summaraized_title[:70] + "..."
        post["title"] = summaraized_title
        post["body"] = twitter_tweet["text"]

        post["comments_count"] = twitter_tweet["retweet_count"]
        post["likes_count"] = twitter_tweet["favorite_count"]

        post["media_type"] = twitter_tweet["media_type"]

        if file_name is not None:
            post["media_url"] = "/content/twitter/" + twitter_tweet["id_str"] + "/" + file_name
            post["media_width"] = twitter_tweet['extended_entities']['media'][0]["sizes"]['medium']["w"]
            post["media_height"] = twitter_tweet['extended_entities']['media'][0]["sizes"]['medium']["h"]
            post["media_aspect_ratio"] = post["media_width"] / post["media_height"]
        else:
            post["media_url"] = None
            post["media_width"] = None
            post["media_height"] = None
            post["media_aspect_ratio"] = None

        post["thumbnail"] = twitter_tweet.get("thumbnail", [])

        post["source_date"] = time.mktime(time.strptime(twitter_tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))
        if file_name is not None:
            extended_entities = twitter_tweet["extended_entities"]
            if twitter_tweet["extended_entities"].get("media") is not None:
                post["source_media_url"] = extended_entities["media"][0]["expanded_url"]

        else:
            if twitter_tweet["entities"].get("mdeia") is not None:
                post["source_media_url"] = twitter_tweet["entities"]["mdeia"]["mediaurl"]
            else:
                if len(twitter_tweet["entities"]["urls"]) > 0:
                    post["source_media_url"] = twitter_tweet["entities"]["urls"][0]["expanded_url"]
                else:
                    post["source_media_url"] = None

        post["source_owner_id"] = twitter_tweet["user"]["id_str"]
        post["source_owner_alias"] = twitter_tweet["user"]["screen_name"]
        post["source_owner_title"] = twitter_tweet["user"]["name"]

        post["language"] = twitter_tweet["lang"]
        post["source"] = 3

        if twitter_tweet.get("urls_extracted") is not None:
            post["urls_extracted"] = twitter_tweet["urls_extracted"]

        self.main_repository.upsert_post(post,custom_hashtags)
