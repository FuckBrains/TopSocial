# from elasticsearch import Elasticsearch
# es = Elasticsearch()
#
# es.indices.create(index='my-index',ignore=400)
import os
import urllib

testfile = urllib.URLopener()
filename = os.path.realpath('insta/BKzoS4kgfEa/BKzoS4kgfEa.jpg')
testfile.retrieve(
    'https://igcdn-photos-g-a.akamaihd.net/hphotos-ak-xfp1/t51.2885-15/s750x750/sh0.08/e35/14474416_1096649077086406_5084599477205991424_n.jpg?ig_cache_key=MTM0NzU5NzkzMzA2Njk3MzQ2Ng%3D%3D.2',
    filename)
