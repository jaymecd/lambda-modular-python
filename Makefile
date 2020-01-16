MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help clean

## display this help
help:
	@ echo 'Usage: make <target>'
	@ echo
	@ echo 'Available targets are:'
	@ awk '/^[[:alnum:]]+([\.\-_][[:alnum:]]*)*:/ { \
			if (match(line, /^## (.*)/)) { printf "    %s,%s\n", substr($$1, 0, index($$1, ":")-1), substr(line, RSTART + 3, RLENGTH); } \
		} { line = $$0 }' $(MAKEFILE_LIST) | sort | column -t -s,
	@ echo

deps:
	### $@
	command -v docker
	command -v sam
	command -v tree

	docker pull lambci/lambda:build-python3.7
	docker pull lambci/lambda:python3.7

## clean up
clean:
	### $@
	find . -mindepth 2 -maxdepth 2 -name Makefile -exec dirname {} \; | xargs -r -I{} make -C {} $@
