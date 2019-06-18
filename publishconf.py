#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = "https://karpoke.ignaciocano.com"
RELATIVE_URLS = False

FEED_RSS = "feeds/rss.xml"
# if FEED_ALL_RSS is set it'll show up in the social bar
FEED_ALL_RSS = "feeds/all/rss.xml"
AUTHOR_FEED_RSS = "feeds/author/{slug}/rss.xml"
CATEGORY_FEED_RSS = "feeds/category/{slug}/rss.xml"
TAG_FEED_RSS = "feeds/tag/{slug}/rss.xml"
FEED_MAX_ITEMS = 10

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

# disable cache when experimenting with different settings
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True
