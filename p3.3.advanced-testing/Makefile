MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help clean build test verify invoke-sam

## display this help
help:
	@ echo 'Usage: make <target>'
	@ echo
	@ echo 'Available targets are:'
	@ awk '/^[[:alnum:]]+([\.\-_][[:alnum:]]*)*:/ { \
			if (match(line, /^## (.*)/)) { printf "    %s,%s\n", substr($$1, 0, index($$1, ":")-1), substr(line, RSTART + 3, RLENGTH); } \
		} { line = $$0 }' $(MAKEFILE_LIST) | sort | column -t -s,
	@ echo

## build lambda using own controlled process
build:
	### $@
	time make -C myfunction build
	tree -a
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - requires contract-based design (framework)'
	@ echo '  - requires to use "aws cloudformation package" to upload code'
	@ echo

## run tests locally
test:
	python3.7 -m unittest discover -s myfunction/test -v

## run docker
verify:
	### $@
	time make -C myfunction verify
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - requires contract-based design (framework)'
	@ echo

## run sam local invoke
invoke-sam:
	### $@
	time sam local invoke --skip-pull-image --no-event MyFunction

## clean up
clean:
	### $@
	find . -type f -name '*.pyc' -print0 | xargs -r -0 rm -rf
	find . -type d -name '__pycache__' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.dist-info' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.egg-info' -print0 | xargs -r -0 rm -rf
	rm -rf .aws-sam
	make -C myfunction $@
