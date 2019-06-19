#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u"Ignacio Cano"
SITENAME = u"Karpoke"
SITEURL = "/"

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
LINKS_WIDGET_NAME = "enlaces"
LINKS = (
    ("Ignacio Cano", "https://www.ignaciocano.com"),
)

# Social widget
SOCIAL = (
    ('github', 'http://github.com/karpoke'),
)

# pagination
DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 5

PAGINATION_PAGE_URL = "{base_name}/pagina/{number}/"
PAGINATION_PAGE_SAVE_AS = "{}index.html".format(PAGINATION_PAGE_URL)
PAGINATION_PATTERNS = (
    (1, "{url}", "{save_as}"),
    (2, PAGINATION_PAGE_URL, PAGINATION_PAGE_SAVE_AS),
)

# url patterns
ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{}index.html".format(ARTICLE_URL)
AUTHOR_URL = "autor/{slug}/"
AUTHOR_SAVE_AS = "{}index.html".format(AUTHOR_URL)
AUTHORS_URL = "autores/"
AUTHORS_SAVE_AS = "{}index.html".format(AUTHORS_URL)
CATEGORY_URL = "categoria/{slug}/"
CATEGORY_SAVE_AS = "{}index.html".format(CATEGORY_URL)
CATEGORIES_URL = "categorias/"
CATEGORIES_SAVE_AS = "{}index.html".format(CATEGORIES_URL)
TAG_URL = "etiqueta/{slug}/"
TAG_SAVE_AS = "{}index.html".format(TAG_URL)
TAGS_URL = "etiquetas/"
TAGS_SAVE_AS = "{}index.html".format(TAGS_URL)
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{}index.html".format(PAGE_URL)
ARCHIVES_URL = "archivos/"
ARCHIVES_SAVE_AS = "{}index.html".format(ARCHIVES_URL)
YEAR_ARCHIVE_SAVE_AS = "{}{{date:%Y}}/index.html".format(ARCHIVES_URL)
MONTH_ARCHIVE_SAVE_AS = "{}{{date:%Y}}/{{date:%m}}/index.html".format(ARCHIVES_URL)
DAY_ARCHIVE_SAVE_AS = "{}{{date:%Y}}/{{date:%m}}/{{date:%d}}/index.html".format(ARCHIVES_URL)

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
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

# control whether all pages are displayed in the primary navigation menu
# DISPLAY_PAGES_ON_MENU = True

STATIC_CHECK_IF_MODIFIED = False

# github ribbon
GITHUB_URL = "https://github.com/karpoke/karpoke.github.io"
