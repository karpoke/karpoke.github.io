PY?=python
PELICAN?=pelican
PELICAN_OPTS=

BASE_DIR=$(CURDIR)
INPUT_DIR=$(BASE_DIR)/content
OUTPUT_DIR=$(BASE_DIR)/output
CONFIG_FILE=$(BASE_DIR)/pelicanconf.py
PUBLISHCONF=$(BASE_DIR)/publishconf.py

GITHUB_PAGES_BRANCH=master
DEVELOP_BRANCH=develop
TRAVIS_BRANCH=release

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICAN_OPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICAN_OPTS += --relative-urls
endif

IGNORE_CACHE ?= 0
ifeq ($(IGNORE_CACHE), 1)
	PELICAN_OPTS += --ignore-cache
endif

PELICAN_DEFAULT=$(PELICAN) $(INPUT_DIR) -o $(OUTPUT_DIR) $(PELICAN_OPTS)
PELICAN_DEFAULT_DEV=$(PELICAN_DEFAULT) -s $(CONFIG_FILE)

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make clean                          remove the generated files         '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make regenerate                     regenerate files upon modification '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make publish                        generate using production settings '
	@echo '   make github                         upload the web site via gh-pages   '
	@echo '   make travis                         upload the web site via travis ci  '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo 'Set the IGNORE_CACHE variable to 1 to ignore cache files                  '
	@echo '                                                                          '

clean:
	[ ! -d $(OUTPUT_DIR) ] || rm -rf $(OUTPUT_DIR)

html:
	$(PELICAN_DEFAULT_DEV)

regenerate:
	$(PELICAN_DEFAULT_DEV) -r

serve:
ifdef PORT
	$(PELICAN_DEFAULT_DEV) -l -p $(PORT)
else
	$(PELICAN_DEFAULT_DEV) -l
endif

serve-global:
ifdef SERVER
	$(PELICAN_DEFAULT_DEV) -l -p $(PORT) -b $(SERVER)
else
	$(PELICAN_DEFAULT_DEV) -l -p $(PORT) -b 0.0.0.0
endif

devserver:
ifdef PORT
	$(PELICAN_DEFAULT_DEV) -lr -p $(PORT)
else
	$(PELICAN_DEFAULT_DEV) -lr
endif

publish:
	$(PELICAN_DEFAULT) -s $(PUBLISHCONF)

github: publish
	ghp-import -m "Generate Pelican site" -b $(GITHUB_PAGES_BRANCH) $(OUTPUT_DIR)
	git push origin $(GITHUB_PAGES_BRANCH)

travis:
	git checkout $(TRAVIS_BRANCH)
	git pull
	git merge --no-ff $(DEVELOP_BRANCH) -m"Merge branch '$(DEVELOP_BRANCH)' into '$(TRAVIS_BRANCH)'"
	git push
	git checkout $(DEVELOP_BRANCH)

.PHONY: help clean html regenerate serve serve-global devserver publish github travis
