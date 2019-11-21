#!/usr/bin/env sh

BASIC_PACKAGES="pelican markdown ghp-import typogrify beautifulsoup4 css-html-js-minify"

if command -v pipenv > /dev/null; then
    pipenv update
else
    pip install --upgrade "$BASIC_PACKAGES"
fi
