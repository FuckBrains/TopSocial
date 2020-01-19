class SeoUrl:
    def __init__(self):
        self.excluded_parameters = {
            "و"
        }

    excluded_parameters = {}

    def seo_friendly_url(self, title):
        if title is None:
            title = "post-detail"
        title = title.replace("\n", "") \
            .replace(".", " ") \
            .replace("،", " ") \
            .replace(",", " ") \
            .replace("&", "") \
            .replace("%", "") \
            .replace("?", "") \
            .replace("|", " ") \
            .replace("|", " ") \
            .replace("^", " ") \
            .replace("}", " ") \
            .replace("{", " ") \
            .replace("]", " ") \
            .replace("[", " ") \
            .replace("~", " ") \
            .replace("`", " ") \
            .replace("\\", " ") \
            .replace("=", " ") \
            .replace(":", " ") \
            .replace("@", " ") \
            .replace(";", " ") \
            .replace("/", " ") \
            .replace("#", " ")\
            .replace("(", " ")\
            .replace(")", " ")

        splited_string = title.strip().split(" ")
        cleaned_list = [i for j, i in enumerate(splited_string) if j not in self.excluded_parameters]
        return "-".join(cleaned_list)
