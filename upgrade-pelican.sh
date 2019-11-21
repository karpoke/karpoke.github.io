#!/usr/bin/env sh

BASIC_PACKAGES="pelican markdown ghp-import typogrify beautifulsoup4 css-html-js-minify"

if command -v pipenv > /dev/null; then
    pipenv update
    pipenv run pip freeze | grep -v "pkg-resources" > requirements.txt
else
    pip install --upgrade "$BASIC_PACKAGES"
    pip freeze | grep -v "pkg-resources" > requirements.txt
fi
