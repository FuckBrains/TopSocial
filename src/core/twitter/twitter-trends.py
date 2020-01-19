#!/usr/bin/python

# -----------------------------------------------------------------------
# twitter-trends
#  - lists the current global trending topics
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
    auth=OAuth(
        config["access_key"],
        config["access_secret"],
        config["consumer_key"],
        config["consumer_secret"])
)

# -----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/rest/reference/get/trends/place
# -----------------------------------------------------------------------
results = twitter.trends.place(_id=23424851)

print("UK Trends")

for location in results:
    for trend in location["trends"]:
        print(" - %s" % trend["name"])
