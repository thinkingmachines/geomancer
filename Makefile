.PHONY: build dev travis
build: venv requirements.txt
	venv/bin/pip-sync
dev: venv requirements-dev.txt tests/data/source.sqlite
	venv/bin/pip-sync requirements-dev.txt
travis: requirements-dev.txt tests/data/source.sqlite
	pip install -r requirements-dev.txt
venv:
	python3 -m venv venv
	venv/bin/pip3 install pip-tools
requirements.txt: requirements.in
	venv/bin/pip-compile -o requirements.txt \
	--no-header \
	--no-annotate \
	--no-index \
	--no-emit-trusted-host \
	requirements.in
requirements-dev.txt: requirements-dev.in
	venv/bin/pip-compile -o requirements-dev.txt \
	--no-header \
	--no-annotate \
	--no-index \
	--no-emit-trusted-host \
	requirements-dev.in
tests/data/source.sqlite:
	wget -O $@ --show-progress https://storage.googleapis.com/tm-geomancer/test/source.sqlite
