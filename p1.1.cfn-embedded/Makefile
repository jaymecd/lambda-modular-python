MAKEFLAGS += --warn-undefined-variables
SHELL := sh
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: help clean code sam docker

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
	time sam local invoke --skip-pull-image --no-event MyFunction || :
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - slower that docker, as of runtime, handler & path autodiscovery'
	@ echo '  - sam does not support AWS::Lambda::Function with ZipFile'
	@ echo

code/index.py:
	@ make code
	mv code/lambda0.py $@

## run docker
run-docker: code/index.py
	### $@
	time docker run --rm \
		-v "$(CURDIR)/code:/var/task" \
		"lambci/lambda:python3.7" \
		"index.lambda_handler"
	@ echo
	@ echo '-----'
	@ echo 'CONS:'
	@ echo '  - requires to know upfront: runtime, handler & path'
	@ echo '  - requires to extract code from CFN template'
	@ echo '  - hard to deal with multiple functions'
	@ echo

EXTRACTOR_BIN := extractor/extract_cfn_lambda

$(EXTRACTOR_BIN):
	### $@
	printf '[install]\nprefix=\n' > setup.cfg
	pip3 install -t $(dir $@) git+https://github.com/intuit/cfn_lambda_extractor | grep -i install
	mv $(dir $@)/bin/cfn_lambda_extractor $@
	rm -f setup.cfg

## extract lambda code
code: $(EXTRACTOR_BIN)
	### $@
	mkdir -p code
	find code -name '*.pyc' -delete
	$(EXTRACTOR_BIN) -p lambda -c template.yaml -o code
	find code -type f | sed -e 's/^/ - /'

## clean up
clean:
	### $@
	find . -type f -name '*.pyc' -print0 | xargs -r -0 rm -rf
	find . -type d -name '__pycache__' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.dist-info' -print0 | xargs -r -0 rm -rf
	find . -type d -name '*.egg-info' -print0 | xargs -r -0 rm -rf
	rm -rf $(dir $(EXTRACTOR_BIN)) setup.cfg code
