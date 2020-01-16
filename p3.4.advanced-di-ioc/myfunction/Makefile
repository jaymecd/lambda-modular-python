MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all

RUNTIME := python
VERSION := 3.7

# @see https://gist.github.com/gene1wood/06a64ba80cf3fe886053f0ca6d375bc0#how-to-correctly-solve-the-problem
CODE_NAMESPACE := app
LAMBDA_HANDLER := $(CODE_NAMESPACE).main.lambda_handler

PYTHON := $(RUNTIME)$(VERSION)

TEST_DIR = test
SRC_DIR = src
DIST_DIR = dist

# docker image repo prefix
X_DOCKER_URI ?=
DOCKER_URI = $(if $(X_DOCKER_URI),$(X_DOCKER_URI:/=)/,)
# docker images
DOCKER_BUILD_IMAGE = $(DOCKER_URI)lambci/lambda:build-$(RUNTIME)$(VERSION)
DOCKER_CHECK_IMAGE = $(DOCKER_URI)lambci/lambda:$(RUNTIME)$(VERSION)

.PHONY: help all deps build verify clean .build .test .dist .clean

## display this help
help:
	@ echo 'Usage: make <target>'
	@ echo
	@ echo 'Available targets are:'
	@ awk '/^[[:alnum:]]+([\.\-_][[:alnum:]]*)*:/ { \
			if (match(line, /^## (.*)/)) { printf "    %s,%s\n", substr($$1, 0, index($$1, ":")-1), substr(line, RSTART + 3, RLENGTH); } \
		} { line = $$0 }' $(MAKEFILE_LIST) | sort | column -t -s,
	@ echo

## Build and verify package
all: build verify

## Install build dependencies
deps:
	### $@
	docker pull $(DOCKER_BUILD_IMAGE)
	docker pull $(DOCKER_CHECK_IMAGE)

## Run build in docker. Optional: X_DOCKER_URI=private-repo-uri
build:
	### $@
	docker run --rm -v "$(CURDIR):/var/task" $(DOCKER_BUILD_IMAGE) make .dist

## Verify simulation in docker
verify:
	### $@
	docker run --rm -v "$(CURDIR)/$(DIST_DIR):/var/task" "$(DOCKER_CHECK_IMAGE)" "$(LAMBDA_HANDLER)" '{}'

## Clean files
clean: .clean
	### $@
	rm -rf $(DIST_DIR)

## [internal] clean up temp files
.clean:
	### $@
	find . -type f -name '*.pyc' -print0 | xargs -r -0 rm -rf
	find . -type d \( -name '__pycache__' -o -name '*.dist-info' -o -name '*.egg-info' \) -print0 | xargs -r -0 rm -rf

## [internal] build sources
.build: clean
	### $@
	mkdir -p $(DIST_DIR)
	cp -r $(SRC_DIR) $(DIST_DIR)/$(CODE_NAMESPACE)
	$(PYTHON) -m pip install -U -t $(DIST_DIR)/ -r requirements.txt

## [internal] execute tests
.test: .build
	### $@
	$(PYTHON) -m unittest discover -t . -s $(TEST_DIR) -v

## [internal] prepare for packaging
.dist: .test
	### $@
	make .clean
	rm -rf $(DIST_DIR)/bin/ $(DIST_DIR)/*.dist-info $(DIST_DIR)/*.egg-info

	find $(DIST_DIR) -exec touch -a -m -t 01010000.00 {} +
