#!/usr/bin/python

# -----------------------------------------------------------------------
# twitter-user-timeline
#  - displays a user's current timeline.
# -----------------------------------------------------------------------
import os

from past.builtins import execfile
from twitter import *



proxy = 'http://ir236996:711278@us.mybestport.com:443'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy


# -----------------------------------------------------------------------
# load our API credentials 
# -----------------------------------------------------------------------
config = {}
execfile("config.py", config)

# -----------------------------------------------------------------------
# create twitter API object
# -----------------------------------------------------------------------
twitter = Twitter(
    auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

# -----------------------------------------------------------------------
# this is the user we're going to query.
# -----------------------------------------------------------------------
user = "ideoforms"

# -----------------------------------------------------------------------
# query the user timeline.
# twitter API docs:
# https://dev.twitter.com/rest/reference/get/statuses/user_timeline
# -----------------------------------------------------------------------
results = twitter.statuses.user_timeline(screen_name=user)

# -----------------------------------------------------------------------
# loop through each status item, and print its content.
# -----------------------------------------------------------------------
for status in results:
    print("(%s) %s" % (status["created_at"], status["text"].encode("ascii", "ignore")))
