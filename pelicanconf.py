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

# url patterns
INDEX_SAVE_AS = "index.html"

PAGINATION_PAGE_URL = "{base_name}/pagina/{number}/"
PAGINATION_PAGE_SAVE_AS = "{}{}".format(PAGINATION_PAGE_URL, INDEX_SAVE_AS)
PAGINATION_PATTERNS = (
    (1, "{url}", "{save_as}"),
    (2, PAGINATION_PAGE_URL, PAGINATION_PAGE_SAVE_AS),
)

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{}{}".format(ARTICLE_URL, INDEX_SAVE_AS)
AUTHOR_URL = "autor/{slug}/"
AUTHOR_SAVE_AS = "{}{}".format(AUTHOR_URL, INDEX_SAVE_AS)
AUTHORS_URL = "autores/"
AUTHORS_SAVE_AS = "{}{}".format(AUTHORS_URL, INDEX_SAVE_AS)
CATEGORY_URL = "categoria/{slug}/"
CATEGORY_SAVE_AS = "{}{}".format(CATEGORY_URL, INDEX_SAVE_AS)
CATEGORIES_URL = "categorias/"
CATEGORIES_SAVE_AS = "{}{}".format(CATEGORIES_URL, INDEX_SAVE_AS)
TAG_URL = "etiqueta/{slug}/"
TAG_SAVE_AS = "{}{}".format(TAG_URL, INDEX_SAVE_AS)
TAGS_URL = "etiquetas/"
TAGS_SAVE_AS = "{}{}".format(TAGS_URL, INDEX_SAVE_AS)
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{}{}".format(PAGE_URL, INDEX_SAVE_AS)
ARCHIVES_URL = "archivos/"
ARCHIVES_SAVE_AS = "{}{}".format(ARCHIVES_URL, INDEX_SAVE_AS)
YEAR_ARCHIVE_URL = "{date:%Y}/"
YEAR_ARCHIVE_SAVE_AS = "{}{}".format(YEAR_ARCHIVE_URL, INDEX_SAVE_AS)
MONTH_ARCHIVE_URL = "{}{{date:%m}}/".format(YEAR_ARCHIVE_URL, INDEX_SAVE_AS)
MONTH_ARCHIVE_SAVE_AS = "{}{}".format(MONTH_ARCHIVE_URL, INDEX_SAVE_AS)
# Used only if you have the {url} placeholder in PAGINATION_PATTERNS
DAY_ARCHIVE_URL = "{}{{date:%d}}/".format(MONTH_ARCHIVE_URL)
DAY_ARCHIVE_SAVE_AS = "{}{}".format(DAY_ARCHIVE_URL, INDEX_SAVE_AS)

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
MLOAD_CONTENT_CACHE = False
CACHE_CONTENT = False

# control whether all pages are displayed in the primary navigation menu
# DISPLAY_PAGES_ON_MENU = True

STATIC_CHECK_IF_MODIFIED = False

# github ribbon
GITHUB_URL = "https://github.com/karpoke/karpoke.github.io"
