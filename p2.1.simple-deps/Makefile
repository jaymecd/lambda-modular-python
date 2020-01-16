MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help clean build-sam verify-sam build-docker verify-docker

## display this help
help:
	@ echo 'Usage: make <target>'
	@ echo
	@ echo 'Available targets are:'
	@ awk '/^[[:alnum:]]+([\.\-_][[:alnum:]]*)*:/ { \
			if (match(line, /^## (.*)/)) { printf "    %s,%s\n", substr($$1, 0, index($$1, ":")-1), substr(line, RSTART + 3, RLENGTH); } \
		} { line = $$0 }' $(MAKEFILE_LIST) | sort | column -t -s,
	@ echo

## install deps using sam
build-sam:
	### $@
	time sam build --skip-pull-image --use-container MyFunction
	tree -a
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - build process is not controllable'
	@ echo '  - uses .aws-sam/build magic directory'
	@ echo

## run sam local invoke
verify-sam:
	### $@
	time sam local invoke --skip-pull-image --no-event MyFunction
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - slower that docker, as of runtime, handler & path autodiscovery'
	@ echo '  - uses .aws-sam/build magic directory'
	@ echo

## install deps using docker
build-docker:
	### $@
	time docker run --rm \
		-v "$(CURDIR)/myfunction:/var/task" \
		lambci/lambda:build-python3.7 \
		pip3 install -U -t ./ -r requirements.txt
	tree -a
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - requires to know upfront: runtime & path'
	@ echo '  - source path becomes dirty'
	@ echo

## run docker
verify-docker:
	### $@
	time docker run --rm \
		-v "$(CURDIR)/myfunction:/var/task" \
		"lambci/lambda:python3.7" \
		"index.lambda_handler"
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - requires to know upfront: runtime, handler & path'
	@ echo

## clean up
clean:
	### $@
	find . -type f -name '*.pyc' -print0 | xargs -r -0 rm -rf
	find . -type d -name '__pycache__' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.dist-info' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.egg-info' -print0 | xargs -r -0 rm -rf
	rm -rf .aws-sam myfunction/yaml/
