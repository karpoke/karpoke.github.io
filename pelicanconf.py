#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u"Ignacio Cano"
SITENAME = u"Karpoke"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Madrid"

DEFAULT_LANG = u"es"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Ignacio Cano", "https://www.ignaciocano.com"),
)

# Social widget
SOCIAL = (
    ('github', 'http://github.com/karpoke'),
)

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 5
PAGINATION_PATTERNS = (
    (1, "{url}", "{save_as}"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# to use a custom domain in github pages
STATIC_PATHS = [
    "extra/CNAME", 
    "extra/favicon.ico",
    "extra/humans.txt",
    "extra/robots.txt",
]
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/humans.txt": {"path": "humans.txt"},
    "extra/robots.txt": {"path": "robots.txt"},
}

# disable cache when experimenting with different settings
LOAD_CONTENT_CACHE = False

# control whether all pages are displayed in the primary navigation menu
# DISPLAY_PAGES_ON_MENU = True

STATIC_CHECK_IF_MODIFIED = False

GITHUB_URL = "https://github.com/karpoke/karpoke.github.io"
