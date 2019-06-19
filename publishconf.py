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

FEED_URL = "feeds/"
FEED_SAVE_AS = "rss.xml"
FEED_RSS = "{}{}".format(FEED_URL, FEED_SAVE_AS)
# if FEED_ALL_RSS is set it'll show up in the social bar
FEED_ALL_RSS = "{}all/{}".format(FEED_URL, FEED_SAVE_AS)
AUTHOR_FEED_RSS = "{}{}{}".format(FEED_URL, AUTHOR_URL, FEED_SAVE_AS)
CATEGORY_FEED_RSS = "{}{}{}".format(FEED_URL, CATEGORY_URL, FEED_SAVE_AS)
TAG_FEED_RSS = "{}{}{}".format(FEED_URL, TAG_URL, FEED_SAVE_AS)
FEED_MAX_ITEMS = 10

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
