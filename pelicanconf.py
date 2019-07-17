#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u"Nacho Cano"
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
    ("Pelican", "https://blog.getpelican.com/"),
    ("Python", "https://www.python.org/"),
    ("Travis CI", "https://travis-ci.org/"),
    ("ImgBot", "https://imgbot.net/"),
)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/karpoke'),
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
MONTH_ARCHIVE_URL = "{}{{date:%m}}/".format(YEAR_ARCHIVE_URL)
MONTH_ARCHIVE_SAVE_AS = "{}{}".format(MONTH_ARCHIVE_URL, INDEX_SAVE_AS)
# Used only if you have the {url} placeholder in PAGINATION_PATTERNS
DAY_ARCHIVE_URL = "{}{{date:%d}}/".format(MONTH_ARCHIVE_URL)
DAY_ARCHIVE_SAVE_AS = "{}{}".format(DAY_ARCHIVE_URL, INDEX_SAVE_AS)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PAGE_EXCLUDES = ["extra"]
ARTICLE_EXCLUDES = PAGE_EXCLUDES

# CNAME: to use a custom domain in github pages
# .nojekyll: to bypass Jekyll in GHP:
# https://github.blog/2009-12-29-bypassing-jekyll-on-github-pages/
STATIC_PATHS = [
    "images",
    "deb",
    "extra/CNAME",
    "extra/LICENSE",
    "extra/README.md",
    "extra/.nojekyll",
    "extra/favicon.ico",
    "extra/humans.txt",
    "extra/robots.txt",
    "extra/.imgbotconfig",
]
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/LICENSE": {"path": "LICENSE"},
    "extra/README.md": {"path": "README.md"},
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/.nojekyll": {"path": ".nojekyll"},
    "extra/humans.txt": {"path": "humans.txt"},
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/.imgbotconfig": {"path": ".imgbotconfig"},
}

# disable cache when experimenting with different settings
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

STATIC_CHECK_IF_MODIFIED = False

# control whether all pages are displayed in the primary navigation menu
# DISPLAY_PAGES_ON_MENU = True

# github ribbon
GITHUB_URL = "https://github.com/karpoke/karpoke.github.io"
