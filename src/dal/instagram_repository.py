from core.function.string_handler import StringHandler
from dal.main_repository import *
from core.nlp.summerize_text import *


class instagram_repository:
    main_repository = ""
    string_handler=""

    def __init__(self):
        self.main_repository = main_repository()
        self.string_handler = StringHandler()

    def upsert_instagram_post(self, instagram_post, file_name):
        post = {}
        post["id"] = instagram_post["id"]
        instagram_post["body"] = self.string_handler.remove_atsigns(instagram_post["body"])
        summaraized_title = summerize_text(instagram_post["body"])._text if summerize_text(
            instagram_post["body"]) is not None else None
        if summaraized_title is not None and len(summaraized_title) > 70:
            summaraized_title = summaraized_title[:70] + "..."
        post["title"] = summaraized_title
        post["body"] = instagram_post["body"]

        post["comments_count"] = instagram_post["comments"]
        post["likes_count"] = instagram_post["likes"]

        post["media_type"] = instagram_post["media_type"]
        post["media_url"] = "/content/insta/" + instagram_post["id"] + "/" + file_name
        post["media_width"] = instagram_post['dimensions']['width']
        post["media_height"] = instagram_post['dimensions']['height']
        post["media_aspect_ratio"] = post["media_width"] / post["media_height"]

        post["thumbnail"] = instagram_post["thumbnail"]

        post["source_date"] = instagram_post["date"]
        post["source_media_url"] = instagram_post["mediaurl"]
        post["source_owner_id"] = instagram_post["ownerid"]
        post["source_owner_alias"] = instagram_post["page"]
        post["source_owner_title"] = instagram_post["page"]

        post["language"] = "fa"
        post["source"] = 1

        self.main_repository.upsert_post(post)
