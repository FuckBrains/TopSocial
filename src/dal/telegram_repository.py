from dal.main_repository import *


# from core.function.url_handler import *

class telegram_repository:
    main_repository = ""

    def __init__(self):
        self.main_repository = main_repository()

    def upsert_telegram_post(self, telegram_post, file_name, media):
        post = {}
        post["id"] = media[
            "id"]  # str(telegram_post['forward_from_chat']["id"]) + "_" + str(telegram_post['message_id'])
        post["title"] = media["title"]
        post["body"] = media["body"]

        post["comments_count"] = 0
        post["likes_count"] = 0

        post["media_type"] = media["media_type"]
        post["media_url"] = "/content/telegram/" + post["id"] + "/" + file_name if file_name is not None else None
        post["media_width"] = media.get("media_width")
        post["media_height"] = media.get("media_height")
        post["media_aspect_ratio"] = media.get("media_aspect_ratio")

        post["thumbnail"] = media.get("thumbnail", [])

        post["source_date"] = telegram_post["date"].timestamp()
        post["source_media_url"] = telegram_post.video.file_id if telegram_post.video is not None else None
        post[
            "source_owner_id"] = telegram_post.forward_from_chat.id if telegram_post.forward_from_chat is not None else None
        post[
            "source_owner_alias"] = telegram_post.forward_from_chat.username if telegram_post.forward_from_chat is not None else None
        post[
            "source_owner_title"] = telegram_post.forward_from_chat.title if telegram_post.forward_from_chat is not None else None

        post["language"] = "fa"
        post["source"] = 2

        self.main_repository.upsert_post(post)
