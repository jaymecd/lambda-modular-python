MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help clean run-sam run-docker

## display this help
help:
	@ echo 'Usage: make <target>'
	@ echo
	@ echo 'Available targets are:'
	@ awk '/^[[:alnum:]]+([\.\-_][[:alnum:]]*)*:/ { \
			if (match(line, /^## (.*)/)) { printf "    %s,%s\n", substr($$1, 0, index($$1, ":")-1), substr(line, RSTART + 3, RLENGTH); } \
		} { line = $$0 }' $(MAKEFILE_LIST) | sort | column -t -s,
	@ echo

## run sam local invoke
run-sam:
	### $@
	time sam local invoke --skip-pull-image --no-event MyFunction
	tree -a
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - slower that docker, as of runtime, handler & path autodiscovery'
	@ echo

## run docker
run-docker:
	### $@
	time docker run --rm \
		-v "$(CURDIR)/code:/var/task" \
		"lambci/lambda:python3.7" \
		"index.lambda_handler"
	tree -a
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
