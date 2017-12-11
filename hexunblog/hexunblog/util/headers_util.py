import random


class HeadersUtil(object):
    ua_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
    ]

    def __init__(self):
        pass

    @classmethod
    def get_default_headers(cls):
        user_agent = random.choice(cls.ua_pool)
        headers = {
            "User-Agent": user_agent,
        }
        return headers

    @classmethod
    def get_article_headers(cls):
        user_agent = random.choice(cls.ua_pool)
        headers = {
            "User-Agent": user_agent,
        }
        return headers
