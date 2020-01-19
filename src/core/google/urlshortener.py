import os

import requests
import json


class GoogleUrlShortener:
    # def __init__(self):


    def goo_shorten_url(self,url):
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key='
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        return r.json()['id']
